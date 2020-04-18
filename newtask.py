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


# creating an object of the EVehicle class

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


    def delete_entity(self, newtask):
        newtaskName = self.request.get('taskname')
        if newtaskName:
            newtaskKey = ndb.Key('TASKMyUser', newtaskName)
            newtask = newtaskKey.get()
            if self.request.get('delete') == 'true':
                newtaskName.key.delete()
                


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

        newtask.put()

    def getAll():
        return TASKMyUser.query().fetch_page(PAGE_SIZE)

    def byName(taskname):
        newtaskKey = ndb.Key('TASKMyUser', taskname)
        return newtaskKey.get()


# EVList
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


# EVCompare
# Function: get
# Function to handle HTTP get request to display a form with all TASKMyUsers with checkbox
# Function; post
# Function to handle HTTP post request to compare given GPUs and  diaplays in a table


class EVCompare(webapp2.RequestHandler):
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

        newtasks, nextCursor, more = EVMyUser.query().fetch_page(PAGE_SIZE)
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'newtasks': newtasks
        }
        template = JINJA_ENVIRONMENT.get_template('ev-compare-form.html')
        self.response.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()
        template_values = {}
        if user:
            url = users.create_logout_url('/')
            url_string = 'logout'
        else:
            self.redirect(users.create_login_url('/'))
            return
        newtask = self.request.params.getall('newtask')
        if len(newtask) != 2:
            message = ''
            if (len(newtask) < 2):
                message = 'Select 2 EVMyUsers to compare'
            elif len(newtask) > 2:
                message = 'Select at most 2 EVMyUsers to compare'

            template = JINJA_ENVIRONMENT.get_template('error.html')
            self.response.write(template.render({'message': message}))
            return
        newtaskKey = ndb.Key('EVMyUser', newtask[0])
        newtask1 = newtaskKey.get()
        newtaskKey = ndb.Key('EVMyUser', newtask[1])
        newtask2 = newtaskKey.get()
        template = JINJA_ENVIRONMENT.get_template('ev-compare.html')
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'newtask1': newtask1,
            'newtask2': newtask2
        }
        self.response.write(template.render(template_values))


# EVSearch
# Function: get
#   Function to handle HTTP get request
#   Display the EVMyUsers satisfied by the search conditions from the user as hyperlinks

class EVSearch(webapp2.RequestHandler):
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
        query = EVMyUser.query()
        search = {}
        if self.request.get('taskname'):
            query = query.filter(EVMyUser.taskname == taskname)
            search['taskname'] = taskname

        newtasks, nextCursor, more = query.fetch_page(PAGE_SIZE)
        for newtask in newtasks:
            print newtask.taskname
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'newtasks': newtasks,
            'search': search
        }
        template = JINJA_ENVIRONMENT.get_template('ev-search.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/newtask', TASKMyUsers),
    ('/newtask/list', TASKList)
], debug=True)
