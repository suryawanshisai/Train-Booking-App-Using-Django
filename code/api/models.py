from django.db import models

from db_connect import db

users_collection = db['users']
train_collection = db['trains']
booking_collection = db['bookings']

