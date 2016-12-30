from my_website_handler import MyBlogWebsiteHandler


class LogOut(MyBlogWebsiteHandler):
    def get(self):
        self.response.headers.add_header("Set-Cookie",
                                         "%s=%s; Path=/" % ("user_cookie_id",
                                                            "deleted; Expires=Thu, 01-Jan-1970 00:00:00 GMT"))
        self.redirect("/login")
