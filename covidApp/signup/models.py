from django.db import models
from mongoengine import *


class Account(Document):
    userEmail = StringField(max_length=50)
    firstName = StringField(max_length=100)
    lastName = StringField(max_length=100)
    password = StringField(max_length=50)
    country = StringField(max_length=20)
