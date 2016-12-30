from google.appengine.ext import db


class Comment(db.Model):
    blog_id = db.IntegerProperty(required=True)
    user_id = db.IntegerProperty(required=True)
    comment = db.StringProperty(required=True)

    @classmethod
    def comment_on_blog(cls, blog_id, logged_in_user_id, user_comment):
        new_comment = Comment(blog_id=blog_id,
                              user_id=logged_in_user_id,
                              comment=user_comment)
        new_comment.put()

    @classmethod
    def get_recent_comments_on_blog(cls, blog_id):
        comment_row = cls.all().filter("blog_id", int(blog_id))
        return comment_row

    @classmethod
    def delete_comments_by_blog_id(cls, blog_id):
        comments_to_delete = cls.all().filter("blog_id", int(blog_id))
        db.delete(comments_to_delete)

    @classmethod
    def delete_comment_by_comment_id(cls, comment_id):
        comment_to_delete = cls.get_by_id(int(comment_id))
        db.delete(comment_to_delete)

    @classmethod
    def update_comment(cls, comment_id, comment_update):
        comment_to_edit = cls.get_by_id(int(comment_id))
        comment_to_edit.comment = comment_update
        comment_to_edit.put()
