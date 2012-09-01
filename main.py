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

from google.appengine.api import users

import gaejson

from models import Lesson

class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<a href="/app/index.html">App Here</a>')

class LessonHandler(webapp2.RequestHandler):
  def return_json(self, object):
    data = gaejson.encode(object)
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    self.response.out.write(data)
    
  def get(self, arg=None):
    #TODO: Security
    user = users.get_current_user()
    if arg is None:
      #GET /lessons
      lessons = Lesson.all().fetch(100) #TODO: limit & paginate
    else:
      #GET /lessons/:keys
      keys = arg.split(',')
      lessons = Lesson.get(keys)
      if len(lessons) == 1:
        lessons = lessons[0]
    
    self.return_json(lessons)
    
  def post(self, key=None):
    #TODO: Security
    user = users.get_current_user()
    data = json.loads(self.request.body)
    
    if key is None:
      lesson = Lesson(name=data['name'])
    else:
      lesson = Lesson.get(key)
      
    for field, value in data.items():
      # TODO: All these special cases are results of the logic in gaejson.encode().  We should put together something to decode that output back into gae stuff
      
      # Keys are special!
      if field == 'key':
        if value != key:
          #TODO: Raise some sort of error.  You can write attributes to a URL without specifying the key, but if you pass a different key in the JSON than in the URL, that's cause for alarm
          pass
      else:
        # Users are special!
        if isinstance(getattr(lesson, field), users.User):
          email = value['email']
          auth_domain = value['auth_domain']
          value = users.User(email=email, _auth_domain=auth_domain)
          
        setattr(lesson, field, value)
      
    lesson.put()
    self.return_json(lesson)
    
  def delete(self, key):
    #TODO: Security
    user = users.get_current_user()
    lesson = Lesson.get(arg)
    lesson.delete()
    self.response.set_status(204)

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/lessons', LessonHandler),
                               ('/lessons/(.*)', LessonHandler),
                              ], debug=True)
