import os
import webapp2
import jinja2
import time
from hasher import Hasher


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

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
        cookie_secure_value = Hasher.make_secure_cookie(cookie_value)
        self.response.headers.add_header(
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
        # self.logged_in_user = user_cookie_id and User.get_row_by_id(user_cookie_id)]
