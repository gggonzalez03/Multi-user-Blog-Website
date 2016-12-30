from google.appengine.ext import db
from hasher import Hasher


class User(db.Model):
    username = db.StringProperty(required=True)
    hashed_password = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def get_row_by_id(cls, user_id):
        retrieved_user = cls.get_by_id(int(user_id))
        return retrieved_user

    @classmethod
    def get_row_by_username(cls, username):
        retrieved_user = cls.all().filter('username', username).get()
        return retrieved_user

    @classmethod
    def register(cls, username, password, email=None):
        # hash password and then return a User object
        hashed_password = Hasher.make_salted_hash(username, password)

        return User(username=username,
                    hashed_password=hashed_password,
                    email=email)
