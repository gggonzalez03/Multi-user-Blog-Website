from google.appengine.ext import db


class Blog(db.Model):
    """Creates an entity for storing blog information
    in the google datastore.
    """
    user_id = db.IntegerProperty(required=True)
    blog_title = db.StringProperty(required=True)
    blog_body = db.TextProperty(required=True)
    date_posted = db.DateTimeProperty(auto_now_add=True)
    date_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def post_blog(cls, user_id, blog_title, blog_body):
        """Adds a blog entry in the Blog table in the database

        The database creates a new row to with the parameters from
        this function.

        Args:
            user_id: The user_id(as integer) of the author of the blog post
            blog_title: The title of the blog in string
            blog_body: The body of the blog in string
                (preferably a string type that preserves white spaces)
        """
        return Blog(user_id=user_id,
                    blog_title=blog_title,
                    blog_body=blog_body)

    @classmethod
    def get_recent_blogs(cls):
        """Retrieves the 10 latest blogs in the database

        Gets data from the database table "Blog" and convert it
        to a python usable list of dictionaries
        """
        # this function returns the 10 most recent blogs in the database
        recent_blogs = cls.all().order('-date_posted').run(limit=10)
        return recent_blogs

    @classmethod
    def get_all_blogs_by_user(cls, user_id):
        """Retrieves all blogs that a specific user posted

        Gets data from the database table "Blog" and convert it
        to a python usable list of dictionaries

        Args:
            user_id: The user_id of author of the posts
        """
        # this function returns all the blogs of a certain user
        all_user_blogs = cls.all().filter("user_id", user_id)
        return all_user_blogs

    @classmethod
    def get_blog_by_blog_id(cls, blog_id):
        """Retrieves a specific blog using a blog_id

        Gets data from the Blog entity and return it as
        a dictionary

        Args:
            blog_id: The id of the blog that is being retrieved
        """
        blog = cls.get_by_id(int(blog_id))
        return blog

    @classmethod
    def delete_a_blog(cls, blog_id):
        """Deletes a specific blog

        Deteles a single entry in Blog entity from the database

        Args:
            blog_id: The id of the blog that is being deleted
        """
        # this function deletes a blog entry from the database
        # assign the blog to be deleted to a variable called blog
        blog = cls.get_blog_by_blog_id(blog_id)
        db.delete(blog)
