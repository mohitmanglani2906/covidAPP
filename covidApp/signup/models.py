from django.db import models
from mongoengine import *
import datetime

class Account(Document):
    userEmail = StringField(max_length=50)
    firstName = StringField(max_length=100)
    lastName = StringField(max_length=100)
    password = StringField(max_length=200)
    country = StringField(max_length=20)

class UserToken(Document):
    token = StringField(max_length=200)
    userEmail = StringField(max_length=50)
    lastUpdated = DateTimeField(default=datetime.datetime.now())