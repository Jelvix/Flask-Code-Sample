import flask
from flask import Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_raw_jwt
from jsonref import requests
from werkzeug.exceptions import BadRequest

from server.user.google_auth import constants
from server.user.google_auth.credentials_editions import credentials_to_dict
from server.user.models.user import User, UserRole
from server.extensions import jwt
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient import discovery

google_blueprint = Blueprint('google_auth', __name__, )

# TODO blacklist into redis
blacklist = set()


@google_blueprint.route('/current_user_creation')
def current_user_creation():
    """
    This endpoint check if user is added into admins and update info about user from google
    :return: status, access_token
    """
    try:
        if 'credentials' not in flask.session:
            return BadRequest('User need to login')

        # Load credentials from the session.
        credentials = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])
        oauth2_client = discovery.build(
            constants.API_SERVICE_NAME, constants.API_VERSION, credentials=credentials)
        flask.session['credentials'] = credentials_to_dict(credentials)
        response = oauth2_client.userinfo().v2().me().get().execute()
    except:
        raise BadRequest('You need to refresh google auth token')
    email = response['email']
    if not User.query.first():
        user = User(email=email)
        first_roles = ['owner', 'exchanges', 'logbook', "user management"]
        roles = initialize_some_roles(first_roles)
        for role in roles:
            user.add_role(role_name=role.role_name)
        user.save()
        print(user.roles)
    if User.query.filter_by(email=email).first():
        user = User.query.filter_by(email=email).first()
        if not user.is_active:
            return "User is not active", 403
        if user.first_name is None:
            user.first_name = response['given_name']
            user.full_name = user.get_full_name()
        if user.last_name is None:
            user.last_name = response['family_name']
            user.full_name = user.get_full_name()
        if user.avatar_url is None:
            user.avatar_url = response['picture']
        user.save()
        access_token = create_access_token(identity=email)
        return flask.jsonify(access_token=access_token), 200
    else:
        return "User with this email is not registered by admin.", 403


@google_blueprint.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        constants.CLIENT_SECRETS_FILE, scopes=constants.SCOPES)

    flow.redirect_uri = flask.url_for('google_auth.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@google_blueprint.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        constants.CLIENT_SECRETS_FILE, scopes=constants.SCOPES, state=state)
    flow.redirect_uri = flask.url_for('google_auth.oauth2callback', _external=True)
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    return flask.redirect(flask.url_for('google_auth.current_user_creation'))


@google_blueprint.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return 'You need to <a href="/authorize">authorize</a> before '

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return 'Credentials successfully revoked.'
    else:
        return BadRequest('An error occurred.')


@google_blueprint.route('/logout')
@jwt_required
def clear_credentials_logout():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return "Successfully logged out", 200


def initialize_black_list_loader():
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist


def initialize_some_roles(*roles):
    for role in roles:
        new_role = UserRole(role_name=role)
        new_role.save()
    return UserRole.query.all()