# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from models import *

# Create your views here.
### Index renders login/registration page ###
def index(request):
    return render(request, 'belt_app/index.html')

### Registration process --> class User, UserManagers from models.py ###
def register(request):
    errors = User.objects.registration_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        messages.success(request, "Successful registration bro")
        User.objects.new_user(request.POST)
        return redirect('/')

### Method redirects to the initial book page ###
### Display all reviews in queryset ###
def book(request):
    user = User.objects.get(id = request.session['user_id'])
    reviews = Review.objects.order_by('-created_at')[:3]
    context = {
            'reviews': reviews,
            'user': user
        }
    return render(request, 'belt_app/books.html', context)

def book_info(request, id):
    book = Book.objects.get(id = id)
    reviews = Review.objects.all()
    context = {
        'book': book,
        'reviews': reviews
    }

    return render(request, 'belt_app/book_info.html', context)

def delete(request, id):
    review = Review.objects.get(id = id)
    review.delete()

    return redirect('/books')

### Login process --> class User, UserManager from models.py ###
def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) is list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    else:
        user = User.objects.login_user(request.POST)
        request.session['user_id'] = user.id

        print request.session['user_id']
        
        return redirect('/books')

### Method renders add_book template with user.id ###
def add(request, id):
    return render(request, 'belt_app/new_book.html')

### Adding new book and book review process ###
def add_process(request, id):
    errors = Book.objects.book_validation(request.POST)
    if errors[0]:
        for error in errors:
            messages.error(request, error)
        return render(request, 'belt_app/new_book.html')
    else:
        result = Book.objects.new_book(request.POST)
        
        # ## GET book from class Book ##
        # booky = Book.objects.get(title = request.POST['book_title'], author = request.POST['author'])
        ## Add book_review through 'BOOKY' ###
        result.book_reviews.create(review = request.POST['review'], stars = request.POST['stars'], user_id = request.session['user_id'])

        this_book = Book.objects.get(title = request.POST['book_title'])

        reviews = result.book_reviews.all().count()
        context = {
            'book': this_book,
            'reviews': reviews
        }

        return render(request, 'belt_app/book_info.html', context)

def add_comment(request, id):
    this_book = Book.objects.get(id = id)
    this_user = User.objects.get(id = request.session['user_id'])
    Review.objects.create(review = request.POST['review'], stars = request.POST['stars'], user = this_user, book = this_book)

    return redirect('/book/(?P<id>\d+)$')

### User information ###
def user_info(request, id):
    user_info = User.objects.get(id = id)
    reviews = Review.objects.filter(user = user_info).count()
    reviewed_books = Review.objects.filter(user = user_info)

    context = {
        'user': user_info,
        'total_reviews': reviews,
        'reviewed_books': reviewed_books
    }

    return render(request, 'belt_app/user_info.html', context)


### logs user out and returns them to registration/login page ###
def logout(request):
    request.session.flush()
    return redirect('/')
