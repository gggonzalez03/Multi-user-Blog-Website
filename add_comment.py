from my_website_handler import MyBlogWebsiteHandler
from comment import Comment


class AddComment(MyBlogWebsiteHandler):
    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")
        if user_id:
            self.redirect("/home")
        else:
            self.redirect("/login")

    def post(self):
        add_comment = self.request.get("addcomment")
        to_delete_or_not = self.request.get("toDeleteCommentOrNot")
        user_id = self.read_secure_cookie("user_cookie_id")

        if user_id:
            if add_comment:
                blog_id = self.request.get("blogid")
                blog_owner_id = self.request.get("ownerid")
                user_comment = self.request.get("usercomment")
                Comment.comment_on_blog(int(blog_id),
                                        int(user_id),
                                        user_comment)
                self.exec_delay()
                self.redirect("/home")
            elif to_delete_or_not:
                if to_delete_or_not == "Yes":
                    comment_id = self.request.get("commentId")
                    Comment.delete_comment_by_comment_id(comment_id)
                    self.exec_delay()
                    self.redirect("/home")
                elif to_delete_or_not == "Edit":
                    comment_id = self.request.get("commentId")
                    comment_update = self.request.get("commentupdate")

                    Comment.update_comment(comment_id, comment_update)

                    self.exec_delay()
                    self.redirect("/home")
                elif to_delete_or_not == "No":
                    self.redirect("/home")
        else:
            self.redirect("/login")
