from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z0-9]\W+$')


class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=post_data['email'])) > 0:
            # check this user's password
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw((post_data['password'].encode()), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')
        if errors:
            return errors
        return user


    def validate_registration(self, post_data):
        errors = {}
        # check all fields for emptyness
        for field, value in post_data.iteritems():
            if len(value) < 1:
                errors[field] = "{} field is reqired".format(
                    field.replace('_', ' '))

            # check name fields for min length
            if field == "name":
                if not field in errors and len(value) < 2:
                    errors[field] = "{} field must bet at least 2 characters".format(
                        field.replace('_', ' '))
                if not field in errors and re.match(NAME_REGEX, field):
                    errors[field] = "{} field must bet only letters".format(
                        field.replace('_', ' '))
            if field == "password":
                if not field in errors and len(value) < 8:
                    errors[field] = "{} field must bet at least 8 characters".format(
                        field.replace('_', ' '))
            if field == "date":
                print field
                print value
                if not field in errors:
                    date_format = "%Y-%m-%d"
                    input_date = datetime.strptime(value, date_format).date()
                    constant_date = datetime.strptime("2017-01-01", date_format).date()
                    deff = constant_date - input_date                    
                    print deff.days
                    if deff.days < 3650:
                        errors[field] = "you must bet at least 11 years old"  

        return errors
    # check email field for valid email
    def validate_login(self, post_data):
        errors = {}
        for field, value in post_data.iteritems():
            if len(value) < 1:
                errors[field] = "{} field is reqired".format(
                    field.replace('_', ' '))
            
            if field == 'email':
                # if not "email" in errors and post_data['email'] != User.objects.get(email=value):
                #     errors[field] = "{} is not correct".format(
                #         field.replace('_', ' '))
                
                if not "email" in errors and not re.match(EMAIL_REGEX, value):
                    errors['email'] = "invalid email/password"

                # if email is valid check db for existing email
                else:
                    if len(self.filter(email=post_data['email'])) > 1:
                        errors['email'] = "email already in use"
        return errors
    #check quote validation
    def validate_quote(self,post_data):
        errors = {}
        for field, value in post_data.iteritems():
            if field == 'quoted_by':
                if len(value) < 3:
                    errors[field] = "{} field must bet at least 4 characters".format(
                        field.replace('_', ' '))
            if field == 'new_quote':                
                if len(value) < 10:
                    errors[field] = "{} field must bet at least 11 characters".format(
                        field.replace('_', ' '))
        return errors
                    
                    
        

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Quote(models.Model):
    quoted_by = models.CharField(max_length = 255)
    quote = models.TextField() 
    user = models.ForeignKey(User, related_name="quotes")
    users_favorites = models.ManyToManyField(User, related_name="favorites_quotes")    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
