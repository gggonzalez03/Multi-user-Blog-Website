from google.appengine.ext import db


class Like(db.Model):
    blog_id = db.IntegerProperty(required=True)
    user_id = db.IntegerProperty(required=True)

    @classmethod
    def like_a_blog(cls, blog_id, logged_in_user_id):
        new_like = Like(blog_id=int(blog_id),
                        user_id=int(logged_in_user_id))
        new_like.put()

    @classmethod
    def get_all_blog_likes(cls, blog_id):
        # this function returns all the blogs of a certain user
        all_blog_likes = cls.all().filter("blog_id", int(blog_id))
        return all_blog_likes

    @classmethod
    def check_user_like(cls, blog_id, user_id):
        # function that checks if a certain blog is already liked by a user
        liked_blog = Like.get_all_blog_likes(int(blog_id))

        is_blog_liked = liked_blog.filter("user_id", int(user_id)).get()
        if is_blog_liked:
            return True
        else:
            return False

    @classmethod
    def get_row_by_user_and_blog_id(cls, blog_id, user_id):
        all_blog_likes = cls.get_all_blog_likes(int(blog_id))
        like_row = all_blog_likes.filter("user_id", int(user_id))
        return like_row

    @classmethod
    def delete_a_like(cls, like_row):
        db.delete(like_row)

    @classmethod
    def delete_likes_by_blog_id(cls, blog_id):
        likes_to_delete = cls.all().filter("blog_id", int(blog_id))
        db.delete(likes_to_delete)
