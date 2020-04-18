from google.appengine.ext import ndb


# MyUser
#DataStore Model for User

class MyUser(ndb.Model):
    # email address of this user
    email_address = ndb.StringProperty()
