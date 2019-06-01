"""
Ojects we need for the program
"""
from datetime import datetime

from flask import render_template, redirect, request

from MyFirstBDProject2 import app
from MyFirstBDProject2.models.factory import create_repository


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

   
# -----------------------------------------------
# Data fields and validators of the registration form
# -----------------------------------------------
class RegistrationForm(Form):
    username   = StringField('Username', [
                            validators.Length(min=4, max=25, message='Username must be 4-25 chars long'),
                            validators.DataRequired(message='You must enter a Username')])
    password   = PasswordField('Password', [
                            validators.DataRequired(message='Please enter a password.'),
                            validators.EqualTo('confirm', message='Passwords must match')])
    confirm    = PasswordField('Repeat Password')
    firstname  = StringField('First Name', [validators.Length(min=1, max=35, message='Illegal first name')])
    lastname   = StringField('Last Name', [validators.Length(min=6, max=35, message='Illegal last name')])
    email      = StringField('Email', [
                            validators.Length(min=6, message='Email address too short.'),
                            validators.Email(message='Not a valid email address.'),
                            validators.DataRequired(message='Not a valid email address.')])
    phone     = StringField('Phone', [validators.Length(min=6, max=14, message='Illegal phone number')])
    submit    = SubmitField('Register')

    def validate_email(self, email):
        return True
        #user = User.query.filter_by(email=email.data).first()
        #if user is not None:
        #    raise ValidationError('Please use a different email address.')

# -----------------------------------------------
# -----------------------------------------------
class LoginForm(Form):
    username   = StringField('Username', [
                            validators.Length(min=4, max=25, message='Username must be 4-25 chars long'),
                            validators.DataRequired(message='You must enter a Username')])
    password   = PasswordField('Password', [
                            validators.DataRequired(message='Please enter a password.')])


# -----------------------------------------------
# -----------------------------------------------
class SearchParameters(Form):

    choosedatabase = SelectField(u'Choose Database',  choices=
                                [('https://data.gov.il/api/action/datastore_search?resource_id=01d99090-aee0-45e8-8817-de404371d636&limit=1000', 'Expenditures of the Ministry of Defense 2017-2018'),
                                 ('https://data.gov.il/api/action/datastore_search?resource_id=c59d89ca-f38e-4a6a-b542-4f91054ccdc1&limit=1000', 'Expenditures of the Ministry of Defense 2016')])
