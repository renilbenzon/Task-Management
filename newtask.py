import webapp2
import jinja2
import os
from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb



JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"], autoescape=True)


# TASKMyUser
# Model for ndb with its features

class TASKMyUser(ndb.Model):
    taskname = ndb.StringProperty(indexed=True)
    useraddress = ndb.StringProperty()
    date = ndb.DateProperty()
    details = ndb.StringProperty()
    notes = ndb.StringProperty()
    status= ndb.StringProperty()


class TASKUser(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    emailaddress = ndb.StringProperty()
    task = ndb.StringProperty()


# creating an object of the Task Management System class

# TASKMyUsers
# Function: get
#   HTTP Get request handler to get a TASKMyUser from data store
#   if newtask name is passed as taskname parameter its fethed from the DataStore
#   If edit parameter is passed with value true the data data is displayed in an editable form
# Function: post
#   HTTP post request hander to create or update TASKMyUser to DataStore based on action parameter
# Function: update
#   Function to update the values of the TASKMyUser to DataStore




class TASKMyUsers(webapp2.RequestHandler):

    def get(self,newtask):
        PAGE_SIZE = 50
        user = users.get_current_user()
        template_values = {}
        if user:
            url = users.create_logout_url('/')
            url_string = 'logout'
        else:
            self.redirect(users.create_login_url('/'))
            return

        newtasks, nextCursor, more = TASKMyUser.query().fetch_page(PAGE_SIZE)
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'newtasks': newtasks
        }
        template = JINJA_ENVIRONMENT.get_template('task-user.html')
        self.response.write(template.render(template_values))



        username = self.request.get('username'),
        emailaddress = self.request.get('emailaddress'),
        task = self.request.get('task'),
        task=taskname_key.get()
        newtask.put()


class TASKMyUsers(webapp2.RequestHandler):

    def get(self, *args, **kargs):
        user = users.get_current_user()
        url_string = ''
        if user:
            url = users.create_logout_url('/')
            url_string = 'logout'
        else:
            url_string = 'login'
            self.redirect(users.create_login_url('/'))
            return
        template = JINJA_ENVIRONMENT.get_template('newtask.html')
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'newtask': {},
            'action': 'create',
            'label': 'Add'
        }
        newtaskName = self.request.get('taskname')
        if newtaskName:
            newtaskKey = ndb.Key('TASKMyUser', newtaskName)
            newtask = newtaskKey.get()
            if newtask:
                template_values = {
                    'url': url,
                    'url_string': url_string,
                    'user': user,
                    'newtask': newtask,
                    'action': 'update',
                    'label': 'Update'
                }
                if self.request.get('edit') == 'true':
                    template_values['edit'] = True
            else:
                template = JINJA_ENVIRONMENT.get_template('error.html')
                template_values = {'message': 'Graphic Processing Unit \'' + newtaskName + '\' not found'}
        else:
            template_values['edit'] = True
            if 'newtask' in kargs:
                template_values['newtask'] = newtask
        print template_values
        self.response.write(template.render(template_values))






    def post(self):
        user = users.get_current_user()
        template_values = {}
        if user:
            url = users.create_logout_url(self.request.url)
            url_string = 'logout'
        else:
            self.redirect(users.create_login_url('/'))
            return

        newtaskName = self.request.get('taskname')
        oldName = self.request.get('oldname')
        action = self.request.get('action')

        taskname = self.request.get('taskname'),
        useraddress = self.request.get('useraddress'),
        date = self.request.get('doi'),
        details = self.request.get('details'),
        notes = self.request.get('notes')
        status = self.request.get('status')
        newtaskKey = None
        newtask = None
        if oldName != '':
            newtaskKey = ndb.Key('TASKMyUser', oldName)
            newtask = newtaskKey.get()
        else:
            newtaskKey = ndb.Key('TASKMyUser', newtaskName)
            newtask = newtaskKey.get()
        template_values = {}
        if newtask:
            if action == 'create':
                template_values['message'] = newtaskName + ' already exists'
                template = JINJA_ENVIRONMENT.get_template('error.html')
                self.response.write(template.render(template_values))
                return
            elif action == 'update':
                try:
                    TASKMyUsers.update(self, newtask)
                except ValueError:
                    template_values['message'] = 'Invalid date format'
                    template = JINJA_ENVIRONMENT.get_template('error.html')
                    self.response.write(template.render(template_values))
                    return
                self.redirect('/newtask?taskname=' + oldName)
                return
            else:
                template_values['message'] = 'Not yet supported'
                template = JINJA_ENVIRONMENT.get_template('error.html')
                self.response.write(template.render(template_values))
                return
        else:
            newtask = TASKMyUser(id=newtaskName)
            newtask.taskname = newtaskName
            try:
                TASKMyUsers.update(self, newtask)
            except ValueError:
                template_values['message'] = 'Invalid date format'
                template = JINJA_ENVIRONMENT.get_template('error.html')
                self.response.write(template.render(template_values))
                return
            template_values = {
                'url': url,
                'url_string': url_string,
                'user': user,
                'newtask': newtask,
                'message': 'Saved successfuly'
            }
            self.redirect('/newtask')

    def update(self, newtask):
        newtask.useraddress = self.request.get('useraddress')
        newtask.date = datetime.strptime(self.request.get('doi'), "%Y-%m-%d")
        newtask.details = self.request.get('details')
        newtask.notes = self.request.get('notes')
        if self.request.get('status'):
            newtask.status = "Completed"
        else:
            newtask.status = "Not Completed"
        newtask.put()







    def getAll():
        return TASKMyUser.query().fetch_page(PAGE_SIZE)

    def byName(taskname):
        newtaskKey = ndb.Key('TASKMyUser', taskname)
        return newtaskKey.get()


# TaskList
# Function: get
#   Function to handle HTTP get request
#   Displays all the TASKMyUsers from DataStore as hyperlinks

class TASKList(webapp2.RequestHandler):
    def get(self):
        PAGE_SIZE = 50
        user = users.get_current_user()
        template_values = {}
        if user:
            url = users.create_logout_url('/')
            url_string = 'logout'
        else:
            self.redirect(users.create_login_url('/'))
            return

        newtasks, nextCursor, more = TASKMyUser.query().fetch_page(PAGE_SIZE)
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'newtasks': newtasks
        }
        template = JINJA_ENVIRONMENT.get_template('task-list.html')
        self.response.write(template.render(template_values))




class TaskBoard(webapp2.RequestHandler):
    def get(self):
        PAGE_SIZE = 50
        user = users.get_current_user()
        template_values = {}
        if user:
            url = users.create_logout_url('/')
            url_string = 'logout'
        else:
            self.redirect(users.create_login_url('/'))
            return

        newtasks, nextCursor, more = TASKMyUser.query().fetch_page(PAGE_SIZE)
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'newtasks': newtasks
        }
        template = JINJA_ENVIRONMENT.get_template('task-board.html')
        self.response.write(template.render(template_values))





app = webapp2.WSGIApplication([
    ('/newtask', TASKMyUsers),
    ('/newtask/list', TASKList),
    ('/newtask/board', TaskBoard),
    ('/newtask/user', TASKUser)
], debug=True)
