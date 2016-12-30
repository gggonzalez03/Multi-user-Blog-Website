from my_website_handler import MyBlogWebsiteHandler
from blog import Blog
from comment import Comment
from like import Like


class DeleteBlog(MyBlogWebsiteHandler):
    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")
        if user_id:
            self.redirect("/home")
        else:
            self.redirect("/login")

    def post(self):
        # get data from the form
        # TODO:
            # Delete rows in Likes and Comments table
            # that are associated with the deleted blog
        user_id = self.read_secure_cookie("user_cookie_id")
        blog_id = self.request.get("blogId")

        # Check if the logged in user is the
        # author of the blog being deleted
        if int(user_id) ==  Blog.get_blog_by_blog_id(blog_id).user_id:
            Comment.delete_comments_by_blog_id(blog_id)
            Like.delete_likes_by_blog_id(blog_id)
            Blog.delete_a_blog(blog_id)

            self.exec_delay()

            self.redirect("/home")
        else:
            self.redirect("/login")
