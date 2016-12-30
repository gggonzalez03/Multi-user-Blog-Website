from my_website_handler import MyBlogWebsiteHandler
from input_validators import InputValidators
from user import User


class WelcomePage(MyBlogWebsiteHandler, InputValidators):
    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")
        if user_id:
            self.render("welcome.html",
                            message=User.get_row_by_id(user_id).username,
                            username=User.get_row_by_id(user_id).username)
        else:
            self.redirect("/login")
