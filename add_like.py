from my_website_handler import MyBlogWebsiteHandler
from like import Like


class AddLike(MyBlogWebsiteHandler):
    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")
        if user_id:
            self.redirect("/home")
        else:
            self.redirect("/login")

    def post(self):
        like_blog_post = self.request.get("likeblogpost")# Returns Like or Unlike. From the form
        blog_owner_id = self.request.get("ownerid")
        user_id = self.read_secure_cookie("user_cookie_id")
        if not user_id == blog_owner_id:
            blog_id = self.request.get("blogid")
            # if the user is not the owner, let him like
            if not Like.check_user_like(blog_id, user_id):
                # if the logged in user hasnt already liked the blog
                Like.like_a_blog(blog_id, user_id)

                self.exec_delay()

                self.redirect("/home")
            else:
                # unlike, delete specific row in the Like table
                to_delete_row = Like.get_row_by_user_and_blog_id(blog_id,
                                                                 user_id)
                Like.delete_a_like(to_delete_row)

                self.exec_delay()

                self.redirect("/home")
        else:
            self.render("homepage.html",
                        error_message="You can't like your own posts")
