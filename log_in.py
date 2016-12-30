from my_website_handler import MyBlogWebsiteHandler
from input_validators import InputValidators
from hasher import Hasher
from user import User


class LogIn(MyBlogWebsiteHandler, InputValidators):
    def login_user_via_credentials(self, username, password):
        user_row = User.get_row_by_username(username)
        if user_row:
            # function to check if password and username match
            # get the hashed_password from user_row
            if self.validate_credentials(username, password, user_row.hashed_password):
                # set a secure cookie
                self.set_secure_cookie("user_cookie_id",
                                       str(user_row.key().id()))
                return True
            else:
                return False
        else:
            return False

    def get(self):
        self.render("login.html")

    def post(self):
        has_error = False

        username = self.request.get("username")
        password = self.request.get("password")

        # check if credentials are valid in the first place before checking the database
        if not self.valid_username(username):
            has_error = True

        if not self.valid_password(password):
            has_error = True

        if has_error:
            self.render("login.html",
                        invalid_login_message="Invalid login")
        else:
            # check the database if the user exists
            if self.login_user_via_credentials(username, password):
                self.redirect("/home")
            else:
                self.render("login.html",
                            invalid_login_message="Invalid login")
