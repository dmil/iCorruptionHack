from flask import Flask
import os, sys
import json
from peewee import *

from app import app, db
from models import File, Contribution, ContributionChanges, ContributionHistory
from ingester import seed_from, ingest

def createtables_db():
    # Connect to our database.
    db.connect()

    # Create the tables.
    db.create_tables([Contribution, ContributionChanges, ContributionHistory, File])

    print "Created tables"

def clear_db():
    db.execute_sql('drop schema public cascade; create schema public;')
    print "Cleared database"

def seed_db():
    seed_from("data/downloaded_2014_02_17/itcont_2013_2014.txt")

def reset_database():
    # Drop all tables in postgres database
    clear_db()

    # Create tables
    createtables_db()

    # Seed data
    seed_db()

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'run':

        import views

        app.run(debug=True)
    elif mode == 'reset':
        reset_database()
    elif mode == 'ingest':
        ingest("data/downloaded_2014_09_14/itcont_2013_2014.txt")

