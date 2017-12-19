# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = []
        
        if len(postData['name']) <= 0:
            errors.append("Name field can't be empty")

        if len(postData['alias']) <= 0:
            errors.append("Alias field can't be empty")

        if not EMAIL_REGEX.match(postData['email'].lower()):
            errors.append("Invalid email addresses")
        
        elif User.objects.filter(email = postData['email'].lower()):
            errors.append("Email already registered!")

        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters long")

        elif postData['password'] != postData['passwordcf']:
            errors.append("Passwords do not match")
        
        return errors
    
    def login_validator(self, postData):
        errors = []
        users = self.filter(email = postData['email'])

        if not users:
            errors.append("Email does not exist")
        
        else:
            users = users[0]
            if not bcrypt.checkpw(postData['password'].encode(), users.password.encode()):
                errors.append("Password does not exist")
        
        if not errors:
            return users

        return errors
    
    def new_user(self, postData):
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = hash1)

        return user
    
    def login_user(self, postData):
        user = self.get(email = postData['email'])
        
        return user

class BookManager(models.Manager):
    def book_validation(self, postData):
        errors = []
        if len(postData['book_title']) <= 0:
            errors.append("Book title field can't be empty")
        
        if len(postData['author']) <= 0:
            errors.append("Author field can't be empty")
        
        if Book.objects.filter(title = postData['book_title'], author = postData['author']):
            errors.append("Book and author already registered")
        
        return errors
    
    def new_book(self, postData):
        book = Book.objects.create(title = postData['book_title'], author = postData['author'])

        return book
        
class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)

    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)

    objects = BookManager()

class Review(models.Model):
    review = models.TextField()
    stars = models.IntegerField()
    user = models.ForeignKey(User, related_name = "user_reviews")
    book = models.ForeignKey(Book, related_name = "book_reviews")
    created_at = models.DateTimeField(auto_now_add = True)
