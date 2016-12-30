import re
from hasher import Hasher


class InputValidators:
    # valid input criteria - regular expression
    USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile("^.{3,20}$")
    EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")

    def valid_username(self, username):
        # returns a True if username is valid and False if not
        return username and self.USER_RE.match(username)

    def valid_password(self, password):
        # returns a True if password is valid and False if not
        return password and self.PASS_RE.match(password)

    def valid_email(self, email):
        # returns a True if email is valid and False if not
        return not email or self.EMAIL_RE.match(email)

    def validate_credentials(self, username, password, hashed_password):
        salt = hashed_password.split('|')[0]
        return hashed_password == Hasher.make_salted_hash(username,
                                                          password,
                                                          salt)
