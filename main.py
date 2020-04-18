import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"], autoescape=True)


# MainPage
# Funcion: get
#	Home page for the application
#	Checks user session and creates login logout url accordingly
#	If a new user comes in it is added to the MyUser DataStore

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        # pull the current user from the request
        user = users.get_current_user()
        myuser = None
        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url('/')
            url_string = 'logout'
            myuser_key = ndb.Key("MyUser", user.email())
            myuser = myuser_key.get()
            print myuser
            if myuser == None:
                myuser = MyUser(id=user.email(), email_address=user.email())
                myuser.put()
        else:
            url = users.create_login_url('/')
            url_string = 'login'
        # self.redirect(users.create_login_url(self.request.uri))
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'myuser': myuser
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
