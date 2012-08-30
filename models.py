#!/usr/bin/env python

import json

from google.appengine.ext import db

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
  
class Lesson(db.Model):
  #Parent: Class
  name = db.StringProperty(required=True)
  week = db.ReferenceProperty(Week)
  day = db.IntegerProperty()
  attachments = JsonProperty()