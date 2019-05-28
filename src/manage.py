# manage.py
from flask.cli import FlaskGroup

from server.app import create_app
from server.extensions import db
from server.user.models.user import User

cli = FlaskGroup(create_app=create_app)


@cli.command()
def create_db():
    """drop all data from db and create new db"""
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='ad@min.com', admin=True))
    db.session.commit()


@cli.command()
def create_data():
    """Creates sample data."""
    pass


if __name__ == '__main__':
    cli()
