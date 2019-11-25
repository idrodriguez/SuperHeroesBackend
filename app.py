# # import libraries
from flask import Flask
from flask_pymongo import PyMongo
from envparse import env

# Flask app definition
app = Flask(__name__)
app.config["MONGO_URI"] = env('MONGODB_URI')
mongo = PyMongo(app)