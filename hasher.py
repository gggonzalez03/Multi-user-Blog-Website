import hashlib
import hmac
import string
import random


SECRET_STRING = "thisismyfirstwebsite"


class Hasher:
    @classmethod
    def make_salt(cls):
        return "".join(random.choice(string.letters) for x in xrange(5))

    @classmethod
    def make_salted_hash(cls, username, password, salt=None):
        if not salt:
            salt = cls.make_salt()
        hashed_value = hashlib.sha256(username + password + salt).hexdigest()
        return "%s|%s" % (salt, hashed_value)

    @classmethod
    def make_secure_cookie(cls, user_id):
        # generate a secure cookie via hmac using a secret string
        hashed_user_id = hmac.new(SECRET_STRING, user_id).hexdigest()
        return "%s|%s" % (user_id, hashed_user_id)
