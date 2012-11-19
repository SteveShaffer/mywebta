#!/usr/bin/env python

import json

from google.appengine.ext import db #TODO: Use ndb
from google.appengine.api import users

class MytaModel(db.Model):
  name = db.StringProperty(required=True)
  owner = db.UserProperty(required=True, auto_current_user_add=True)
  def is_users(self):
    return (self.owner == users.get_current_user())

class JsonProperty(db.TextProperty):
  def validate(self, value):
    return value
  
  def get_value_for_datastore(self, model_instance):
    result = super(JsonProperty, self).get_value_for_datastore(model_instance)
    result = json.dumps(result)
    return db.Text(result)
    
  def make_value_from_datastore(self, value):
    try:
      value = json.loads(str(value))
    except:
      pass
    
    return super(JsonProperty, self).make_value_from_datastore(value)

class User(db.Model):
  name = db.StringProperty()
  user = db.UserProperty(required=True, auto_current_user_add=True)
  
class Class(db.Model):
  #Parent: User
  name = db.StringProperty(required=True)
  
class Week(db.Model):
  date = db.DateProperty(required=True)
  #plan = JsonProperty() #Week is outside ancestor path?
  schedule = JsonProperty()
  
class LessonFolder(db.Model):
  #Parent: LessonFolder or Nothing
  owner = db.UserProperty(auto_current_user_add=True) #TODO: required=True
  name = db.StringProperty(required=True)
  lessons = db.ListProperty(db.Key)
  
class Lesson(db.Model):
  #Parent: LessonFolder
  owner = db.UserProperty(auto_current_user_add=True) #TODO: required=True
  name = db.StringProperty(required=True)
  attachments = JsonProperty()
  
class Period(MytaModel):
  pass
  
class Student(MytaModel):
  period = db.ReferenceProperty(Period)
  
class Test(MytaModel):
  content = JsonProperty()
  
class Type(db.Model):
  name = db.StringProperty(required=True)
  attributes = db.BlobProperty()
  
class Thing(db.Model):
  type = db.ReferenceProperty(Type)
  name = db.StringProperty(required=True)
  attributes = db.BlobProperty()