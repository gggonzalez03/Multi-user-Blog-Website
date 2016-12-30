from google.appengine.ext import db


class Blog(db.Model):
    user_id = db.IntegerProperty(required=True)
    blog_title = db.StringProperty(required=True)
    blog_body = db.TextProperty(required=True)
    date_posted = db.DateTimeProperty(auto_now_add=True)
    date_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def post_blog(cls, user_id, blog_title, blog_body):
        return Blog(user_id=user_id,
                    blog_title=blog_title,
                    blog_body=blog_body)

    @classmethod
    def get_recent_blogs(cls):
        # this function returns the 10 most recent blogs in the database
        recent_blogs = cls.all().order('-date_posted').run(limit=10)
        return recent_blogs

    @classmethod
    def get_all_blogs_by_user(cls, user_id):
        # this function returns all the blogs of a certain user
        all_user_blogs = cls.all().filter("user_id", user_id)
        return all_user_blogs

    @classmethod
    def get_blog_by_blog_id(cls, blog_id):
        blog = cls.get_by_id(int(blog_id))
        return blog

    @classmethod
    def delete_a_blog(cls, blog_id):
        # this function deletes a blog entry from the database
        # assign the blog to be deleted to a variable called blog
        blog = cls.get_blog_by_blog_id(blog_id)
        db.delete(blog)
