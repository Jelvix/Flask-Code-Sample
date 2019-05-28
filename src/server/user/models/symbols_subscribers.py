from server.extensions import db

symbol_subscribers = db.Table('symbol_subscribers',
                              db.Column('user_id', db.Integer, db.ForeignKey('users.id'),
                                        primary_key=True),
                              db.Column('currency_pair_id', db.Integer, db.ForeignKey('currency_pair.id'),
                                        primary_key=True)
                              )
