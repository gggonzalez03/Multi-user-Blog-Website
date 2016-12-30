from my_website_handler import MyBlogWebsiteHandler
from user import User
from blog import Blog

class EditBlog(MyBlogWebsiteHandler):
    def update_blog_entry(self, user_id, blog_id, blog_title, blog_body):
        to_edit_blog = Blog.get_blog_by_blog_id(blog_id)
        to_edit_blog.blog_title = blog_title
        to_edit_blog.blog_body = blog_body
        to_edit_blog.put()
        return to_edit_blog.blog_title

    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")
        if user_id:
            self.redirect("/home")
        else:
            self.redirect("/login")

    def post(self):
        post_or_update_blog = self.request.get("postorupdateblog")
        blog_id = self.request.get("blogId")
        blog = Blog.get_blog_by_blog_id(blog_id)
        blog_owner_id = blog.user_id

        if post_or_update_blog == "Edit Post":
            blog_title = blog.blog_title
            blog_body = blog.blog_body
            user_id = self.read_secure_cookie("user_cookie_id")

            if int(user_id) == int(blog_owner_id):
                self.render("editblog.html", blog_id=blog_id,
                            blog_title=blog_title,
                            blog_body=blog_body,
                            username=User.get_row_by_id(user_id).username)
            else:
                self.render("homepage.html",
                            error_message="You can't edit someone else's posts")
        elif post_or_update_blog == "Update Post":
            blog_title = self.request.get("blogTitle")
            blog_body = self.request.get("blogBody")
            user_id = self.read_secure_cookie("user_cookie_id")

            if int(user_id) == int(blog_owner_id):
                self.update_blog_entry(blog_owner_id,
                                       blog_id,
                                       blog_title,
                                       blog_body)

                self.exec_delay()

                self.redirect("/home")
            else:
                self.render("homepage.html",
                            error_message="You can't edit someone else's posts")
