import os
from flask import Flask
import json
from peewee import *

app = Flask(__name__)
root = os.path.dirname(os.path.abspath(__file__))

with open('keys.json','r') as keysfile:
    keys = json.load(keysfile)
    postgres_keys = keys['postgres']
    name = postgres_keys['database']
    del postgres_keys['database']

db = PostgresqlDatabase(name, autocommit=True, **postgres_keys)
