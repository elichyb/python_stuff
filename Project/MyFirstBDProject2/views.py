"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, redirect, request, url_for

from MyFirstBDProject2 import app
from MyFirstBDProject2.models.panda import create_repository

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from MyFirstBDProject2.models.objects import RegistrationForm 
from MyFirstBDProject2.models.objects import LoginForm 
from MyFirstBDProject2.models.objects import SearchParameters 

repository = create_repository()

# -------------------------------------------------------
# transform a picture to a memory represenation of the image
# -------------------------------------------------------
def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue())

# -------------------------------------------------------
# return boolean if username (paramter) is in the Users DB
# -------------------------------------------------------
def IsUserExist(UserName):
    # Load the database of users
    df = repository.OpenUsersDB()
    df = df.set_index('username')
    return (UserName in df.index.values)

# -------------------------------------------------------
# return boolean if username/password pair is in the DB
# -------------------------------------------------------
def IsLoginGood(UserName, Password):
    # Load the database of users
    df = repository.OpenUsersDB()
    df=df.reset_index()
    selection = [UserName]
    df = df[pd.DataFrame(df.username.tolist()).isin(selection).any(1)]

    df = df.set_index('password')
    return (Password in df.index.values)
     
# -------------------------------------------------------
# Add a new user to the DB
# -------------------------------------------------------
def AddNewUser(User):
    # Load the database of users
    df = repository.OpenUsersDB()
    dfNew = pd.DataFrame([[User.username.data, User.password.data,User.email.data,User.phone.data,User.firstname.data,User.lastname.data]], columns=['username', 'password', 'email', 'phone', 'firstname', 'lastname'])
    dfComplete = df.append(dfNew, ignore_index=True)
    repository.WriteToFile_users(dfComplete)

# -------------------------------------------------------
# Page routing - position of the home page
# -------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Data Science Project',
    )

# -------------------------------------------------------
# Page routing - position of the about page
# -------------------------------------------------------
@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='Final Project. Internal Assesment',
        year=datetime.now().year,
        message='Pandas application description.'
    )

# -------------------------------------------------------
# Page routing - position of the contact page
# -------------------------------------------------------
@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        name="Ori R",
        phone="0546642686",
        title='Student name and contact details',
        year=datetime.now().year,
    )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not IsUserExist(form.username.data)):
            AddNewUser(form)
            db_table = ""

            # flash('Thanks for registering NOT exists- '+ form.username.data)
            return render_template('RegisterOK.html', db_table = db_table, template="dashbord-template")
        else:
            # flash('Thanks for registering exists!! - '+ form.username.data)
            form = RegistrationForm(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if (request.method == 'POST' and form.validate()):
        if (IsLoginGood(form.username.data, form.password.data)):
            return redirect('GetParameters')
        else:
            flash('Error in - Username and password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# When a user was qualified o enter the DB page
# he needs to enter some parameters to set the requested
# query
# -------------------------------------------------------
@app.route('/GetParameters', methods=['GET', 'POST'])
def GetParameters():
    form = SearchParameters(request.form)
 
    if (request.method == 'POST' and form.validate()):
            return pandas(form)
 
    return render_template(
            'GetParameters.html',
            form=form,
            title='Enter parameters for data analysis',
            year=datetime.now().year,
            repository_name='Pandas',
            )
# -------------------------------------------------------
# The data analysis page according to the entered parameters
# Get parameters that the user entered
# -------------------------------------------------------
@app.route('/pandas/<form>')
def pandas(form):
    import urllib
    if (form!='None'):
        form = SearchParameters(request.form)
        DBPath ='https://data.gov.il/api/action/datastore_search?resource_id=01d99090-aee0-45e8-8817-de404371d636&limit=100'
    else:
        DBPath ='https://data.gov.il/api/action/datastore_search?resource_id=c59d89ca-f38e-4a6a-b542-4f91054ccdc1&limit=100'
    js = urllib.urlopen(DBPath).read()
    json.loads(js)
    x = json.loads(js)
    ll = []
    for ind in x["result"]["records"]:
        new_db = {}
        new_db[u'\u05e7\u05d5\u05d3 \u05ea\u05db\u05e0\u05d9\u05ea'] = ind[u'\u05e7\u05d5\u05d3 \u05ea\u05db\u05e0\u05d9\u05ea']
        new_db[u'\u05e7\u05d5\u05d3 \u05de\u05d9\u05d5\u05df \u05e8\u05de\u05d4 1'] = ind[u'\u05e7\u05d5\u05d3 \u05de\u05d9\u05d5\u05df \u05e8\u05de\u05d4 1']
        new_db[u'\u05e7\u05d5\u05d3 \u05ea\u05db\u05e0\u05d9\u05ea'] = ind[u'\u05e7\u05d5\u05d3 \u05ea\u05db\u05e0\u05d9\u05ea']
        new_db[u'\u05e7\u05d5\u05d3 \u05d5\u05e9\u05dd \u05de\u05d9\u05d5\u05df \u05e8\u05de\u05d4 1'] = ind[u'\u05e7\u05d5\u05d3 \u05d5\u05e9\u05dd \u05de\u05d9\u05d5\u05df \u05e8\u05de\u05d4 1']
        new_db['expense'] = ind[u'\u05d4\u05d5\u05e6\u05d0\u05d4 \u05e0\u05d8\u05d5']
        ll.append(new_db)

    df = pd.DataFrame.from_dict(ll)
    db_table = df.head(15).to_html(escape=False)

    fig, ax = plt.subplots()
    df[u'\u05e7\u05d5\u05d3 \u05d5\u05e9\u05dd \u05de\u05d9\u05d5\u05df \u05e8\u05de\u05d4 1'].hist()

    encoded = fig_to_base64(fig)
    plot_img = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

    min_expense = df.head(15).get('expense').min()
    max_expense = df.head(15).get('expense').max()
    sum_expense = df.head(15).get('expense').sum()

    return render_template(
        'pandas.html',
        title='Pandas',
        year=datetime.now().year,
        repository_name='Pandas',
        db_table=db_table,
        plot_img=plot_img,
        min=min_expense,
        max=max_expense,
        summry=sum_expense,
    )
