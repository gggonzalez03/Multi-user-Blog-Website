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
                # Makes sure the user is logged in
                # before adding the comment to the database
                if user_id:
                    Comment.comment_on_blog(int(blog_id),
                                            int(user_id),
                                            user_comment)
                    self.exec_delay()
                    self.redirect("/home")
                else:
                    self.redirect("/login")
            elif to_delete_or_not:
                comment_id = self.request.get("commentId")
                # check if logged in user is the
                # owner of the comment being deleted
                # or edited
                if int(user_id) == Comment.get_user_id_by_comment_id(comment_id):
                    if to_delete_or_not == "Yes":
                        Comment.delete_comment_by_comment_id(comment_id)
                        self.exec_delay()
                        self.redirect("/home")
                    elif to_delete_or_not == "Edit":
                        comment_update = self.request.get("commentupdate")

                        Comment.update_comment(comment_id, comment_update)

                        self.exec_delay()
                        self.redirect("/home")
                    else:
                        self.redirect("/home")
                else:
                    self.redirect("/home")
        else:
            self.redirect("/login")
