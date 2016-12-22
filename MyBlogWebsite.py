import os
import string
import webapp2
import re
import jinja2
from google.appengine.ext import db
import hmac
import hashlib
import random


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret_string = "thisismyfirstwebsite"

class Hasher:
    @classmethod
    def make_salt(cls):
        return "".join(random.choice(string.letters) for x in xrange(5))

    @classmethod
    def make_salted_hash(cls, username, password, salt = None):
        if not salt:
            salt = cls.make_salt()
        hashed_value = hashlib.sha256(username + password + salt).hexdigest()
        return "%s|%s" %(salt, hashed_value)
    @classmethod
    def make_secure_cookie(cls, user_id):
        #generate a secure cookie via hmac using a secret string
        hashed_user_id = hmac.new(secret_string, user_id).hexdigest()
        return "%s|%s" %(user_id, hashed_user_id)
        
    

class User(db.Model):
    username = db.StringProperty(required = True)
    hashed_password = db.StringProperty(required = True)
    email = db.StringProperty()

    #PLEASE EVALUATE :)
    #class methods that are accessible by the class instead of the instance of the class
    @classmethod
    def get_row_by_id(cls, id):
        return cls.get_by_id(id)
    
    @classmethod
    def get_row_by_username(cls, username):
        retrieved_user = cls.all().filter('username =', username).get()
        return retrieved_user
    
    @classmethod
    def register(cls, username, password, email = None):
        #todo:
        #hash password and then return a User object
        hashed_password = Hasher.make_salted_hash(username, password)

        return User(username = username,
                    hashed_password = hashed_password,
                    email = email)

#(c)Udacity
class MyBlogWebsiteHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        #load the file and create a jinja template
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    def set_secure_cookie(cls, cookie_name, user_id):
        #this function set a cookie to a secure value using make_secure_cookie function
        cookie_secure_value = Hasher.make_secure_cookie(user_id)
        self.headers.add_header(
            "Set-Cookie",
            "%s=%s; Path=/" %(cookie_name, cookie_secure_value))

class InputValidators:
    #valid input criteria - regular expression
    USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile("^.{3,20}$")
    EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
    
    def valid_username(self, username):
        #returns a True if username is valid and False if not
        return username and self.USER_RE.match(username)
    def valid_password(self, password):
        #returns a True if password is valid and False if not
        return password and self.PASS_RE.match(password)
    def valid_email(self, email):
        #returns a True if email is valid and False if not
        return not email or self.EMAIL_RE.match(email)
    def validate_credentials(self, username, password, hashed_password):
        salt = hashed_password.split('|')[0]
        return hashed_password == Hasher.make_salted_hash(username, password, salt)

class LogIn(MyBlogWebsiteHandler, InputValidators):
    def get(self):
        #set_cookie
        self.render("login.html")
    def post(self):
        #set_cookie
        self.render("login.html")
    def set_secure_cookie(self, cookie_name, user_id):
        #this function set a cookie to a secure value using make_secure_cookie function
        cookie_secure_value = Hasher.make_secure_cookie(user_id)
        self.response.headers.add_header(
            "Set-Cookie",
            "%s=%s; Path=/" %(cookie_name, cookie_secure_value))
    
    def login_user_via_credentials(self, username, password):
        user_row = User.get_row_by_username(username)
        if user_row:
            #function to check if password and username match
            #get the hashed_password from user_row
            if self.validate_credentials(username, password, user_row.hashed_password):
                #set a secure cookie
                self.set_secure_cookie("user_cookie_id", str(user_row.key()))
                return True
            else:
                return False
        else:
            return False

class HomePage(LogIn):
    def get(self):
        self.render("signup.html")
    def post(self):
        has_error =False
        
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_messages = dict(username = username,
                              email = email)

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
            #todo:
                #check if username exists, if so return to the signup page
                #else, hash the password and insert new entry into the database
                #and set a cookie
            #check if user already exists in the database
            user_row = User.get_row_by_username(username)
            if user_row:
                self.render("signup.html", error_username = "That user already exists!")
            else:
                #if the user does not already exists, create a new entry to the database
                new_user = User.register(username, password, email)
                #insert the new entry into the database
                new_user.put()

                #login the new user
                if self.login_user_via_credentials(username, password): #this should return True :(
                    self.render("welcome.html", message = username + ", you are now logged in!")
                else:
                    self.render("signup.html", error_username = "Oops something went wrong")

class WelcomePage(HomePage):
    def get(self):
        self.render("welcome.html", message = str(username.all().get()))


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/signup/welcome', WelcomePage )
    ],debug=True)
