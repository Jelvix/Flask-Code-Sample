from datetime import datetime

# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from server.user.models.symbols_subscribers import symbol_subscribers
from server.extensions import db

from sqlalchemy import exc

from server.utils.base_model import BaseModel


class User(UserMixin, db.Model, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    full_name = db.Column(db.String, nullable=True)
    avatar_url = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    # password_hash = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    # admin = db.Column(db.Boolean, nullable=False, default=False)
    roles = db.relationship('UserRole', secondary='users_user_roles', lazy='dynamic',
                            backref=db.backref('users', lazy=True))
    symbols = db.relationship('CurrencyPair', secondary=symbol_subscribers, lazy='subquery',
                              backref=db.backref('users', lazy=True))

    buy_percentage = db.Column(db.Float, nullable=True, default=0.5)
    sell_percentage = db.Column(db.Float, nullable=True, default=0.5)

    close_bet_interval_in_minutes = db.Column(db.Float, nullable=True, default=10)

    def __repr__(self):
        return '<User {0}>'.format(self.email)

    def add_role(self, role_name):
        try:
            role = UserRole.query.filter_by(role_name=role_name).first()
            if role not in self.roles:
                return self.roles.append(role)
            else:
                return self.roles
        except exc.IdentifierError:
            pass

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def get_user_roles_names_list(self):
        return [each.role_name for each in self.roles]


class UserRole(db.Model, BaseModel):
    """This model created for custom permission
        role_name: is the permissions' name.
                    It can be "owner" or screens' name ("order history") for which user has permission"""

    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String, unique=True, nullable=False)
    roles = db.relationship('User', secondary='users_user_roles', lazy='dynamic',
                            backref=db.backref('user_roles', lazy=True))

    def __repr__(self):
        return '<Role {0}>'.format(self.role_name)


class UserUserRole(db.Model, BaseModel):
    __tablename__ = 'users_user_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'))

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(User, lazy='subquery',
                           backref=db.backref("users_user_roles", cascade="all, delete-orphan", lazy=True))
    user_role = db.relationship(UserRole, lazy='subquery',
                                backref=db.backref("users_user_roles", cascade="all, delete-orphan", lazy=True))
