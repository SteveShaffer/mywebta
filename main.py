#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import json
import random

from google.appengine.api import users
from google.appengine.ext import db

import gaejson

import models

class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect('/app/index.html')

class JsonHandler(webapp2.RequestHandler):
  """A generic handler for a JSON REST API handling CRUD operations on a single
  model type.
  
  Should set self.model to point to the model around which this handler is to
  be based."""
  
  def _create_object(self, data):
    """"Override this method if you have different required attributes that
    need to be set at construction."""
    return self.model(name=data['name'])
    
  def _set_object_properties(self, object, data):
    for field, value in data.items():
      # TODO: All these special cases are results of the logic in gaejson.encode().  We should put together something to decode that output back into gae stuff
      
      # Keys are special!
      if field == 'key':
        if value != str(object.key()):
          #TODO: Raise some sort of error.  You can write attributes to a URL without specifying the key, but if you pass a different key in the JSON than in the URL, that's cause for alarm
          pass
      elif field == 'parent':
        # Can't update parent
        pass
      else:
        # Users are special!
        if isinstance(getattr(object, field), users.User):
          email = value['email']
          auth_domain = value['auth_domain']
          value = users.User(email=email, _auth_domain=auth_domain)
          
        setattr(object, field, value)
  
  def _return_json(self, object):
    data = gaejson.encode(object)
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    self.response.out.write(data)
    
  def _return_forbidden(self):
    self.response.set_status(403)
    self.response.out.write('Your user account is not authorized to access this resource.')
    
  def _return_not_found(self):
    self.response.set_status(404)
  
  def _return_deleted(self):
    self.response.set_status(204)
    
  def get(self, arg=None):
    user = users.get_current_user()
    if arg is None:
      # GET /{object type} = LIST
      objects = self.model.all().filter('owner = ', user).fetch(100) #TODO: limit & paginate
    else:
      # GET /{object type}/:key(s) = READ
      
      #TODO: Doesn't support multiple keys yet. Beginnings below.
      #keys = arg.split(',')
      #objects = self.model.get(keys)
      #if len(objects) == 1:
      #  objects = objects[0]
      objects = self.model.get(arg)
      
      if not objects.is_users():
        self._return_forbidden()
    
    self._return_json(objects)
    
  def post(self, key=None):
    user = users.get_current_user()
    data = json.loads(self.request.body)
    
    if key is None:
      # POST /{object type} = CREATE
      object = self._create_object(data)
    else:
      # POST /{object types}/:key = UPDATE
      object = self.model.get(key)
      if not object.is_users():
        self._return_forbidden()
      
    self._set_object_properties(object ,data)
    object.put()
    self._return_json(object)
    
  def delete(self, arg):
    # POST /{object type}/:key(s) = DELETE
    
    #TODO: Doesn't support multiple keys yet. Beginnings below.
    #keys = arg.split(',')
    #db.delete(keys)
    
    object = self.model.get(arg)
    if not object.is_users():
      self._return_forbidden()
    object.delete()
    self._return_deleted()

class LessonHandler(JsonHandler):
  model = models.Lesson
  
class LessonFolderHandler(JsonHandler):
  model = models.LessonFolder
  
class PeriodHandler(JsonHandler):
  model = models.Period
  
  def delete(self, arg):
    # POST /{object type}/:key(s) = DELETE
    #TODO: Security
    user = users.get_current_user()
    keys = arg.split(',')
    for key in keys:
      period = self.model.get(key)
      students = period.student_set
      db.delete(students)
      period.delete()
    self.response.set_status(204)
  
class PeriodStudentHandler(JsonHandler):
  
  def get(self, periodKey):
    period = models.Period.get(periodKey)
    students = period.student_set.fetch(100) #TODO: 100-student limit here.
    self._return_json(students)
    
  def post(self):
    self._return_not_found()
    
  def delete(self):
    self._return_not_found()
  
class StudentHandler(JsonHandler):
  model = models.Student
  
  def _set_object_properties(self, object, data):
    for field, value in data.items():
      
      # Keys are special!
      if field == 'key':
        if value != str(object.key()):
          #TODO: Raise some sort of error.  You can write attributes to a URL without specifying the key, but if you pass a different key in the JSON than in the URL, that's cause for alarm
          pass
      elif field == 'parent':
        # Can't update parent
        pass
      elif field == 'period':
        # Ignore this
        pass
      else:
        # Users are special!
        if isinstance(getattr(object, field), users.User):
          email = value['email']
          auth_domain = value['auth_domain']
          value = users.User(email=email, _auth_domain=auth_domain)
          
        setattr(object, field, value)
  
class BatchStudentHandler(JsonHandler):
  model = models.Student
  
  def get(self):
    self._return_not_found()
  
  def post(self):
    periodKey = self.request.get('period')
    period = models.Period.get(periodKey)
    names = self.request.get('names').split('\n')
    logging.info('names = ' + str(names))
    students = []
    for name in names:
      student = models.Student(name=name, period=period)
      student.put()
      students.append(student)
    #self._return_json(students)
    self.redirect('/app/index.html#periods/' + periodKey) #TODO: This is VERY inelegant
    
  def delete(self):
    self._return_not_found()
  
class RandomStudentHandler(JsonHandler):
  model = models.Student
  
  def get(self, periodId):
    period = models.Period.get(periodId)
    students = period.student_set.fetch(100)
    logging.info('len(students) = ' + str(len(students)))
    num = random.randrange(0, len(students))
    student = students[num]
    self._return_json(student)
    
  def post(self):
    self._return_not_found()
  
  def delete(self):
    self._return_not_found()

class ThingHandler(JsonHandler):
  def get(self, type_key, key):
    thing = models.Thing.get(key)
    self._return_json(thing)
    #TODO: FINISH
    
  def post(self, type_key, key):
    #TODO: Write
    pass
  
  def delete(self, type_key, key):
    #TODO: Write
    pass
  
class ThingListHandler(JsonHandler):
  def get(self, type_key):
    #TODO: Support queries / security
    type = models.Type.get(type_key)
    things = models.Thing.all().filter('type = ', type).fetch(100) #TODO: paginate & limit
    self._return_json(things)
    
  def post(self, type_key):
    #TODO: Security
    type = models.Type.get(type_key)
    data = json.loads(self.request.body)
    thing = models.Thing(type=type,name=data['name'])
    self._set_object_properties(thing, data)
    thing.put()
    self._return_json(thing) #TODO: Need to redirect?
    
  def delete(self, type_key):
    #TODO: Write
    pass

class LogoutHandler(webapp2.RequestHandler):
  def get(self):
    url = users.create_logout_url('/')
    self.redirect(url)

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/lessons', LessonHandler),
                               ('/lessons/(.*)', LessonHandler),
                               ('/lessonfolders', LessonFolderHandler),
                               ('/lessonfolders/(.*)', LessonFolderHandler),
                               ('/periods', PeriodHandler),
                               ('/periods/(.*)/students/random', RandomStudentHandler),
                               ('/periods/.*/students/(.*)', StudentHandler),
                               ('/periods/(.*)/students', PeriodStudentHandler),
                               ('/periods/(.*)', PeriodHandler),
                               ('/students/batch', BatchStudentHandler),
                               ('/students', StudentHandler),
                               ('/students/(.*)', StudentHandler),
                               ('/logout', LogoutHandler),
                               ('/(.*)/(.*)', ThingHandler),
                               ('/(.*)', ThingListHandler)
                              ], debug=True)
