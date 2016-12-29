import os
import string
import webapp2
import re
import jinja2
from google.appengine.ext import db
import hmac
import hashlib
import random
import time


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

SECRET_STRING = "thisismyfirstwebsite"


class Hasher:
    @classmethod
    def make_salt(cls):
        return "".join(random.choice(string.letters) for x in xrange(5))

    @classmethod
    def make_salted_hash(cls, username, password, salt=None):
        if not salt:
            salt = cls.make_salt()
        hashed_value = hashlib.sha256(username + password + salt).hexdigest()
        return "%s|%s" % (salt, hashed_value)

    @classmethod
    def make_secure_cookie(cls, user_id):
        # generate a secure cookie via hmac using a secret string
        hashed_user_id = hmac.new(SECRET_STRING, user_id).hexdigest()
        return "%s|%s" % (user_id, hashed_user_id)


class User(db.Model):
    username = db.StringProperty(required=True)
    hashed_password = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def get_row_by_id(cls, user_id):
        retrieved_user = cls.get_by_id(int(user_id))
        return retrieved_user

    @classmethod
    def get_row_by_username(cls, username):
        retrieved_user = cls.all().filter('username', username).get()
        return retrieved_user

    @classmethod
    def register(cls, username, password, email=None):
        # hash password and then return a User object
        hashed_password = Hasher.make_salted_hash(username, password)

        return User(username=username,
                    hashed_password=hashed_password,
                    email=email)


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
        comment_row = cls.all().filter("blog_id", blog_id)
        return comment_row

    @classmethod
    def delete_comments_by_blog_id(cls, blog_id):
        comments_to_delete = cls.all().filter("blog_id", int(blog_id))
        db.delete(comments_to_delete)

    @classmethod
    def delete_comment_by_comment_id(comment_id):
        comment_to_delete = cls.get_by_id(comment_id)
        db.delete(comment_to_delete)


# (c)Udacity
class MyBlogWebsiteHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        # load the file and create a jinja template
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, cookie_name, cookie_value):
        # this function sets a secure cookie
        self.cookie_secure_value = Hasher.make_secure_cookie(cookie_value)
        self.headers.add_header(
            "Set-Cookie",
            "%s=%s; Path=/" % (cookie_name, cookie_secure_value))

    def check_valid_cookie(self, cookie_secure_value):
        # returns the user_id if the cookie is valid
        val = cookie_secure_value.split("|")[0]
        if cookie_secure_value == Hasher.make_secure_cookie(val):
            return val
        else:
            return None

    def read_secure_cookie(self, cookie_name):
        cookie_val = self.request.cookies.get(cookie_name)
        return cookie_val and self.check_valid_cookie(cookie_val)

    def exec_delay(self):
        # this is to allow database to store the new data
        # first before redirecting to the homepage
        time.sleep(.5)

    # def initialize(self, *a, **kw):
        # webapp2.RequestHandler.initialize(self, *a, **kw)
        # user_cookie_id = self.read_secure_cookie('user_cookie_id')
        # self.logged_in_user = user_cookie_id and User.get_row_by_id(user_cookie_id)


class LogOut(MyBlogWebsiteHandler):
    def get(self):
        self.response.headers.add_header("Set-Cookie",
                                         "%s=%s; Path=/" % ("user_cookie_id",
                                                            "deleted; Expires=Thu, 01-Jan-1970 00:00:00 GMT"))
        self.redirect("/login")


class InputValidators:
    # valid input criteria - regular expression
    USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile("^.{3,20}$")
    EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")

    def valid_username(self, username):
        # returns a True if username is valid and False if not
        return username and self.USER_RE.match(username)

    def valid_password(self, password):
        # returns a True if password is valid and False if not
        return password and self.PASS_RE.match(password)

    def valid_email(self, email):
        # returns a True if email is valid and False if not
        return not email or self.EMAIL_RE.match(email)

    def validate_credentials(self, username, password, hashed_password):
        salt = hashed_password.split('|')[0]
        return hashed_password == Hasher.make_salted_hash(username,
                                                          password,
                                                          salt)


class PostBlog(MyBlogWebsiteHandler):
    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")

        self.render("postblog.html",
                    username=User.get_row_by_id(user_id).username)

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


class AddLike(MyBlogWebsiteHandler):
    def get(self):
        self.redirect("/home")

    def post(self):
        blog_id = self.request.get("blogid")
        blog_owner_id = self.request.get("ownerid")
        user_id = self.read_secure_cookie("user_cookie_id")
        if not user_id == blog_owner_id:
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


class AddComment(MyBlogWebsiteHandler):
    def get(self):
        self.redirect("/home")

    def post(self):
        blog_id = self.request.get("blogid")
        blog_owner_id = self.request.get("ownerid")
        user_comment = self.request.get("usercomment")
        user_id = self.read_secure_cookie("user_cookie_id")

        if user_id:
            Comment.comment_on_blog(int(blog_id),
                                    int(user_id),
                                    user_comment)

            self.exec_delay()

            self.redirect("/home")
        else:
            self.redirect("/login")


class EditBlog(MyBlogWebsiteHandler):
    def update_blog_entry(self, user_id, blog_id, blog_title, blog_body):
        to_edit_blog = Blog.get_blog_by_blog_id(blog_id)
        to_edit_blog.blog_title = blog_title
        to_edit_blog.blog_body = blog_body
        to_edit_blog.put()
        return to_edit_blog.blog_title

    def get(self):
        blog_id = self.request.get("blogId")
        blog = Blog.get_blog_by_blog_id(blog_id)
        blog_owner_id = blog.user_id
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

    def post(self):
        blog_id = self.request.get("blogId")
        blog = Blog.get_blog_by_blog_id(blog_id)
        blog_owner_id = blog.user_id
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


class DeleteBlog(MyBlogWebsiteHandler):
    def get(self):
        self.redirect("/home")

    def post(self):
        # get data from the form
        # TODO:
            # Delete rows in Likes and Comments table
            # that are associated with the deleted blog

        blog_id = self.request.get("blogId")
        Comment.delete_comments_by_blog_id(blog_id)
        Like.delete_likes_by_blog_id(blog_id)
        Blog.delete_a_blog(blog_id)

        self.exec_delay()

        self.redirect("/home")


class HomePage(MyBlogWebsiteHandler):
    def get(self):
        user_id = self.read_secure_cookie("user_cookie_id")
        if user_id:
            self.render("homepage.html",
                        blogs=Blog.get_recent_blogs(),
                        users=User,
                        likes=Like,
                        comments=Comment,
                        logged_in_user=int(user_id),
                        username=User.get_row_by_id(user_id).username)
        else:
            self.redirect("/signup")


class LogIn(MyBlogWebsiteHandler, InputValidators):
    def login_user_via_credentials(self, username, password):
        user_row = User.get_row_by_username(username)
        if user_row:
            # function to check if password and username match
            # get the hashed_password from user_row
            if self.validate_credentials(username, password, user_row.hashed_password):
                # set a secure cookie
                self.set_secure_cookie("user_cookie_id",
                                       str(user_row.key().id()))
                return True
            else:
                return False
        else:
            return False

    # TO CHECK
    def set_secure_cookie(self, cookie_name, user_id):
        # this function set a cookie to a secure value using make_secure_cookie function
        cookie_secure_value = Hasher.make_secure_cookie(user_id)
        self.response.headers.add_header(
            "Set-Cookie",
            "%s=%s; Path=/" % (cookie_name, cookie_secure_value))

    def get(self):
        self.render("login.html")

    def post(self):
        has_error = False

        username = self.request.get("username")
        password = self.request.get("password")

        # check if credentials are valid in the first place before checking the database
        if not self.valid_username(username):
            has_error = True

        if not self.valid_password(password):
            has_error = True

        if has_error:
            self.render("login.html",
                        invalid_login_message="Invalid login")
        else:
            # check the database if the user exists
            if self.login_user_via_credentials(username, password):
                self.redirect("/home")
            else:
                self.render("login.html",
                            invalid_login_message="Invalid login")


class SignUp(LogIn):
    def get(self):
        self.render("signup.html")

    def post(self):
        has_error = False

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_messages = dict(username=username,
                              email=email)

        if not self.valid_username(username):
            error_messages["error_username"] = "That's not a valid username"
            has_error = True

        if not self.valid_password(password):
            error_messages["error_password"] = "That's not a valid password"
            has_error = True
        else:
            if not password == verify:
                error_messages["error_password"] = "Your passwords didn't match"
                has_error = True

        if not self.valid_email(email):
            error_messages["error_email"] = "That's not a valid email address"
            has_error = True

        if has_error:
            self.render("signup.html", **error_messages)
        else:
            # todo:
                # check if username exists, if so return to the signup page
                # else, hash the password and insert new entry into the database
                # and set a cookie to log the user in

            # check if user already exists in the database
            user_row = User.get_row_by_username(username)
            if user_row:
                self.render("signup.html",
                            error_username="That user already exists!")
            else:
                # if the user does not already exists, create a new entry to the database
                new_user = User.register(username, password, email)
                # insert the new entry into the database
                new_user.put()

                self.set_secure_cookie("user_cookie_id",
                                       str(new_user.key().id()))
                self.redirect("/welcome")


class WelcomePage(SignUp):
    def get(self):
        user_cookie_id = self.request.cookies.get("user_cookie_id")
        if user_cookie_id:
            is_cookie_valid = self.check_valid_cookie(user_cookie_id)
            if is_cookie_valid:
                # if the cookie is valid
                user_id = user_cookie_id.split("|")[0]
                self.render("welcome.html",
                            message=User.get_row_by_id(user_id).username,
                            username=User.get_row_by_id(user_id).username)
            else:
                self.redirect("/signup")
        else:
            self.redirect("/signup")


app = webapp2.WSGIApplication([
    ('/home', HomePage),
    ('/home/like', AddLike),
    ('/home/comment', AddComment),
    ('/editblog', EditBlog),
    ('/deleteblog', DeleteBlog),
    ('/signup', SignUp),
    ('/logout', LogOut),
    ('/login', LogIn),
    ('/postblog', PostBlog),
    ('/welcome', WelcomePage),
    ], debug=True)
