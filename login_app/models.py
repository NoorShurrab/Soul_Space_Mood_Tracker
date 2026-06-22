from django.db import models
import re
from datetime import datetime, date
from django.contrib.auth.hashers import check_password
import bcrypt

# Regular expression for email format validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        
        # 1. First Name Validation
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long."
        elif not postData['first_name'].isalpha():
            errors['first_name'] = "First name must contain letters only."
            
        # 2. Last Name Validation
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long."
        elif not postData['last_name'].isalpha():
            errors['last_name'] = "Last name must contain letters only."
            
        # 3. Email Validation
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format."
        else:
            # Check if email already exists
            email_exists = User.objects.filter(email=postData['email']).exists()
            if email_exists:
                errors['email'] = "This email is already registered."
                
        # 4. Birthday Validation
        if not postData['birthday']:
            errors['birthday'] = "Birthday field is required."
        else:
            input_date = datetime.strptime(postData['birthday'], '%Y-%m-%d').date()
            if input_date >= date.today():
                errors['birthday'] = "Birthday must be in the past."
                
        # 5. Password Validation
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password and password confirmation do not match."
            
        return errors

    def login_validator(self, postData):
        errors = {}
        
        # Search for user by email
        user_list = User.objects.filter(email=postData['email'])
        if not user_list:
            errors['login'] = "Invalid email or password."
        else:
            user = user_list[0]
            # Check encrypted password
            if not check_password(postData['password'], user.password):
                errors['login'] = "Invalid email or password."
                
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    # Link the manager to the model
    objects = UserManager()

