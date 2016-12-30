from my_website_handler import MyBlogWebsiteHandler
from input_validators import InputValidators
from user import User


class SignUp(MyBlogWebsiteHandler, InputValidators):
    def get(self):
        self.render("signup.html")

    def post(self):
        has_error = False

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_messages = dict(username=username,
                              email=email)

        if not self.valid_username(username):
            error_messages["error_username"] = "That's not a valid username"
            has_error = True

        if not self.valid_password(password):
            error_messages["error_password"] = "That's not a valid password"
            has_error = True
        else:
            if not password == verify:
                error_messages["error_password"] = "Your passwords didn't match"
                has_error = True

        if not self.valid_email(email):
            error_messages["error_email"] = "That's not a valid email address"
            has_error = True

        if has_error:
            self.render("signup.html", **error_messages)
        else:
            # todo:
                # check if username exists, if so return to the signup page
                # else, hash the password and insert new entry into the database
                # and set a cookie to log the user in

            # check if user already exists in the database
            user_row = User.get_row_by_username(username)
            if user_row:
                self.render("signup.html",
                            error_username="That user already exists!")
            else:
                # if the user does not already exists, create a new entry to the database
                new_user = User.register(username, password, email)
                # insert the new entry into the database
                new_user.put()

                self.set_secure_cookie("user_cookie_id",
                                       str(new_user.key().id()))
                self.redirect("/welcome")
