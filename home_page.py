from my_website_handler import MyBlogWebsiteHandler
from user import User
from blog import Blog
from like import Like
from comment import Comment


class HomePage(MyBlogWebsiteHandler):
    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")
        if user_id:
            self.render("homepage.html",
                        blogs=Blog.get_recent_blogs(),
                        users=User,
                        likes=Like,
                        comments=Comment,
                        logged_in_user=int(user_id),
                        username=User.get_row_by_id(user_id).username)
        else:
            self.redirect("/login")
