import webapp2
from home_page import HomePage
from add_like import AddLike
from add_comment import AddComment
from edit_blog import EditBlog
from delete_blog import DeleteBlog
from sign_up import SignUp
from log_out import LogOut
from log_in import LogIn
from post_blog import PostBlog
from welcome_page import WelcomePage


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
