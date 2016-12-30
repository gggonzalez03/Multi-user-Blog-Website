from my_website_handler import MyBlogWebsiteHandler
from user import User
from blog import Blog


class PostBlog(MyBlogWebsiteHandler):
    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")
        if user_id:
            self.render("postblog.html",
                    username=User.get_row_by_id(user_id).username)
        else:
            self.redirect("/login")

    def post(self):
        blog_title = self.request.get("blogtitle")
        blog_body = self.request.get("blogbody")
        user_id = self.read_secure_cookie("user_cookie_id")
        has_error = False

        if user_id and not has_error:
            new_blog = Blog.post_blog(int(user_id), blog_title, blog_body)
            # insert the new entry into the database
            new_blog.put()

            self.exec_delay()

            self.redirect("/home")
        else:
            self.render("postblog.html",
                        blogtitle=blog_title)

