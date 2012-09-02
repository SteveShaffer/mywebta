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

import gaejson

#from models import Lesson
#from models import LessonFolder
import models

class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<a href="/app/index.html">App Here</a>')

#class LessonHandler(webapp2.RequestHandler):
#  def return_json(self, object):
#    data = gaejson.encode(object)
#    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
#    self.response.out.write(data)
#    
#  def get(self, arg=None):
#    #TODO: Security
#    user = users.get_current_user()
#    if arg is None:
#      #GET /lessons
#      lessons = Lesson.all().fetch(100) #TODO: limit & paginate
#    else:
#      #GET /lessons/:keys
#      keys = arg.split(',')
#      lessons = Lesson.get(keys)
#      if len(lessons) == 1:
#        lessons = lessons[0]
#    
#    self.return_json(lessons)
#    
#  def post(self, key=None):
#    #TODO: Security
#    user = users.get_current_user()
#    data = json.loads(self.request.body)
#    
#    if key is None:
#      lesson = Lesson(name=data['name'])
#    else:
#      lesson = Lesson.get(key)
#      
#    for field, value in data.items():
#      # TODO: All these special cases are results of the logic in gaejson.encode().  We should put together something to decode that output back into gae stuff
#      
#      # Keys are special!
#      if field == 'key':
#        if value != key:
#          #TODO: Raise some sort of error.  You can write attributes to a URL without specifying the key, but if you pass a different key in the JSON than in the URL, that's cause for alarm
#          pass
#      else:
#        # Users are special!
#        if isinstance(getattr(lesson, field), users.User):
#          email = value['email']
#          auth_domain = value['auth_domain']
#          value = users.User(email=email, _auth_domain=auth_domain)
#          
#        setattr(lesson, field, value)
#      
#    lesson.put()
#    self.return_json(lesson)
#    
#  def delete(self, key):
#    #TODO: Security
#    user = users.get_current_user()
#    lesson = Lesson.get(arg)
#    lesson.delete()
#    self.response.set_status(204)

#class LessonFolderHandler(webapp2.RequestHandler):
#  def return_json(self, object):
#    data = gaejson.encode(object)
#    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
#    self.response.out.write(data)
#    
#  def get(self, arg=None):
#    #TODO: Security
#    user = users.get_current_user()
#    if arg is None:
#      #GET /lessonfolders
#      folders = LessonFolder.all().fetch(100) #TODO: limit & paginate
#    else:
#      #GET /lessonfolders/:keys
#      keys = arg.split(',')
#      folders = LessonFolder.get(keys)
#      if len(folders) == 1:
#        folders = folders[0]
#    
#    self.return_json(folders)
#    
#  def post(self, key=None):
#    #TODO: Security
#    user = users.get_current_user()
#    data = json.loads(self.request.body)
#    
#    if key is None:
#      folder = LessonFolder(name=data['name'])
#    else:
#      folder = LessonFolder.get(key)
#      
#    for field, value in data.items():
#      # TODO: All these special cases are results of the logic in gaejson.encode().  We should put together something to decode that output back into gae stuff
#      
#      # Keys are special!
#      if field == 'key':
#        if value != key:
#          #TODO: Raise some sort of error.  You can write attributes to a URL without specifying the key, but if you pass a different key in the JSON than in the URL, that's cause for alarm
#          pass
#      elif field == 'parent':
#        # Can't update parent
#        pass
#      else:
#        # Users are special!
#        if isinstance(getattr(folder, field), users.User):
#          email = value['email']
#          auth_domain = value['auth_domain']
#          value = users.User(email=email, _auth_domain=auth_domain)
#          
#        setattr(folder, field, value)
#      
#    folder.put()
#    self.return_json(folder)
#    
#  def delete(self, key):
#    #TODO: Security
#    user = users.get_current_user()
#    folder = LessonFolder.get(key)
#    folder.delete()
#    self.response.set_status(204)

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
  
  def _return_deleted(self):
    self.response.set_status(204)
    
  def get(self, arg=None):
    user = users.get_current_user()
    if arg is None:
      # GET /{object type} = READ
      objects = self.model.all().fetch(100) #TODO: limit & paginate
    else:
      # GET /{object type}/:key(s) = LIST
      keys = arg.split(',')
      objects = self.model.get(keys)
      if len(objects) == 1:
        objects = objects[0]
      
    self._return_json(objects)
    
  def post(self, key=None):
    #TODO: Security
    user = users.get_current_user()
    data = json.loads(self.request.body)
    
    if key is None:
      # POST /{object type} = CREATE
      object = self._create_object(data)
    else:
      # POST /{object types}/:key = UPDATE
      object = self.model.get(key)
      
    self._set_object_properties(object ,data)
    
    object.put()
    self._return_json(object)
    
  def delete(self, arg):
    # POST /{object type}/:key(s) = DELETE
    #TODO: Security
    user = users.get_current_user()
    keys = arg.split(',')
    for key in keys:
      self.model.get(key).delete()
    self.response.set_status(204)

class LessonHandler(JsonHandler):
  model = models.Lesson
  
class LessonFolderHandler(JsonHandler):
  model = models.LessonFolder
  
class PeriodHandler(JsonHandler):
  model = models.Period
  
class StudentHandler(JsonHandler):
  model = models.Student
  
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
    pass
  
  def delete(self):
    pass

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/lessons', LessonHandler),
                               ('/lessons/(.*)', LessonHandler),
                               ('/lessonfolders', LessonFolderHandler),
                               ('/lessonfolders/(.*)', LessonFolderHandler),
                               ('/periods', PeriodHandler),
                               ('/periods/(.*)/students/random', RandomStudentHandler),
                               ('/students', StudentHandler),
                               ('/students/(.*)', StudentHandler)
                              ], debug=True)
