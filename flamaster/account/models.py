# from __future__ import absolute_import
import base64
import random
from datetime import datetime
from time import mktime

from sqlalchemy import Table


from flamaster.app import db, app
from flamaster.core.utils import get_hexdigest
from flamaster.core.models import CRUDMixin


class User(db.Model, CRUDMixin):
    """ By default model inherits id and created_at fields from the CRUDMixin
    """
    __tablename__ = 'users'

    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(512))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(15))

    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign key fot the roles link represented by the role attr
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='users')

    addresses = db.relationship('Address', backref=db.backref('user', lazy='dynamic'))

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return "<User: %r>" % self.email

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email.lower()).first()
        if user is not None:
            salt, hsh = user.password.split('$')
            if hsh == get_hexdigest(salt, password):
                return user
        return user

    @classmethod
    def is_unique(cls, email):
        return cls.query.filter_by(email=email).count() == 0

    @classmethod
    def validate_token(cls, token=None):
        if token is not None and '$$' in token:
            key, hsh = token.split('$$')
            user = cls.query.filter_by(email=base64.decodestring(key)).first()
            if user and token == user.create_token():
                return user
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs).set_password('*')
        return instance.save()

    def create_token(self):
        """ creates a unique token based on user last login time and
        urlsafe encoded user key
        """
        ts_datetime = self.logged_at or self.created_at
        ts = int(mktime(ts_datetime.timetuple()))
        key = base64.encodestring(self.email)
        base = "{}{}".format(key, ts)
        salt, hsh = self.password.split('$')
        return "{}$${}".format(key, get_hexdigest(salt, base))

    def set_password(self, raw_password):
        rand_str = lambda: str(random.random())
        salt = get_hexdigest(rand_str(), rand_str())[:5]
        hsh = get_hexdigest(salt, raw_password)
        self.password = '{}${}'.format(salt, hsh)
        return self

    def save(self, commit=True):
        if not self.role_id and self.email not in app.config['ADMINS']:
            self.role = Role.get_or_create(name=app.config['USER_ROLE'])
        elif not self.role and self.email in app.config['ADMINS']:
            self.role = Role.get_or_create(name=app.config['ADMIN_ROLE'])

        return super(User, self).save(commit=commit)


class Address(db.Model, CRUDMixin):
    """ representing address data for users
        By default model inherits id and created_at fields from the CRUDMixin
    """
    __tablename__ = 'addresses'

    city = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    apartment = db.Column(db.String(20))
    zip_code = db.Column(db.String(20))
    type = db.Column(db.Enum('billing', 'delivery', name='addr_types'),
                     nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, **kwargs):
        assert 'city' in kwargs and 'street' in kwargs
        self.type = kwargs.pop('type', 'delivery')
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)

    def __repr__(self):
        return "<Address:('%s','%s')>" % (self.city, self.street)


# association table
role_permissions = Table(
    'role_permissions', db.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permissions_id', db.Integer, db.ForeignKey('permissions.id')))


class Role(db.Model, CRUDMixin):
    """ By default model inherits id and created_at fields from the CRUDMixin
    """
    __tablename__ = 'roles'

    name = db.Column(db.String(255), unique=True, nullable=False)

    permissions = db.relationship('Permissions', secondary=role_permissions,
                                  lazy='dynamic',
                                  backref=db.backref('roles', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role: %r>" % self.name

    @classmethod
    def get_or_create(cls, name=app.config['USER_ROLE']):
        return cls.query.filter_by(name=name).first() or cls.create(name=name)


class Permissions(db.Model, CRUDMixin):
    """ By default model inherits id and created_at fields from the CRUDMixin
    """
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Permissions: %r>" % self.name
