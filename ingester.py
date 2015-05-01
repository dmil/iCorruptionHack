"""
Push new data to sqlite database.
"""
import datetime, os, re

from peewee import *

from app import db

from models import File, Contribution, ContributionChanges, ContributionHistory

from flask_peewee.utils import get_dictionary_from_model

from dateutil.parser import parse as dateparse

def parse_fec_file(infile):
    cycle = re.match(r"^.*(\d{4}_\d{4}).\w{3}$", infile.split("/")[-1], re.I).groups()[0].replace("_", "-")
    date = dateparse(os.path.dirname(infile).split("/")[-1].replace("downloaded_", "").replace("_", "-")).date()
    with open(infile) as f:
        res = [parse_line(line) for line in f]
        return [row_to_dict(val, cycle, date) for val in res]

def parse_line(l):
    vals = l.split('|')
    vals = map(lambda x: None if x=='' else x,vals)
    int_cols = [18-1,21-1] #file num and sub id
    for i in int_cols:
        if vals[i] is not None:
            vals[i] = int(vals[i])
    float_cols = [15-1] #transaction amount
    for i in float_cols:
        if vals[i] is not None:
            vals[i] = float(vals[i])
    date_cols = [14-1] #date
    for i in date_cols:
        vl = vals[i]
        if vl is not None:
            vals[i] = datetime.datetime(month=int(vl[0:2]), day=int(vl[2:4]), year=int(vl[4:8]))
    return vals

def row_to_dict(row, cycle, date):
    return {
        "cycle": cycle,
        "date": date,
        "comittee_id" : unicode(row[0]) if row[0] else None,
        "ammendment_id" : unicode(row[1]) if row[1] else None,
        "report_type" : unicode(row[2]) if row[2] else None,
        "transaction_pgi" : unicode(row[3]) if row[3] else None,
        "image_num" : unicode(row[4]) if row[4] else None,
        "transaction_tp" : unicode(row[5])  if row[5] else None,
        "entity_tp" : unicode(row[6]) if row[6] else None,
        "name" : unicode(row[7]) if row[7] else None,
        "city" : unicode(row[8]) if row[8] else None,
        "state" : unicode(row[9]) if row[9] else None,
        "zip_code" : unicode(row[10]) if row[10] else None,
        "employer" : unicode(row[11]) if row[11] else None,
        "occupation" : unicode(row[12]) if row[12] else None,

        "transaction_id" : unicode(row[16]) if row[16] else None,
        "memo_cd" : unicode(row[18]) if row[18] else None,
        "memo_text" : unicode(row[19]) if row[19] else None,

        "other_id" : unicode(row[15]) if row[15] else None,

        "transaction_date" : row[13],
        "transaction_amount" : float(row[14]),
        "file_num" : row[17],
        "sub_id" : int(row[20])
    }

def ingested(filepath):
    '''Return true if file is already ingested, false otherwise'''
    # TODO: implement better (just checks if file in table right now)
    try:
        myfile = File.get(name=filepath)
        print "%s already in database." % filepath
        return True
    except:
        return False

def seed_from(filepath):
    '''Ingest file into sqlite database'''

    print "Ingesting %s" % filepath
    rows = parse_fec_file(filepath)
    myfile = File.get_or_create(name=filepath)

    for idx in range(0, len(rows), 500):
        print "Inserting row %d of %s" % (idx, filepath)
        rows_subset = rows[idx:idx+500]
        Contribution.insert_many(rows_subset).execute()

def ingest(filepath):
    '''Ingest file into database'''
    print "Ingesting %s" % filepath
    rows = parse_fec_file(filepath)
    myfile = File.get_or_create(name=filepath)

    # check history table to see if this file is done

    with db.transaction():
        for idx, row in enumerate(rows):
            print "Checking row %d of %s" % (idx, filepath)

            try:
                contribution_in_db = Contribution.get(cycle=row['cycle'], sub_id=row['sub_id'])
            except Contribution.DoesNotExist:
                contribution_in_db = None

            # If the row isn't already there, insert it
            if not contribution_in_db:
                print "\tInserting new row %d of %s" % (idx, filepath)
                Contribution.create(**row)
                ContributionHistory.create(date=row['date'], cycle=row['cycle'], sub_id=row['sub_id'])

            # If the row is there, check for modifications
            else:
                # If it has not been modified, simply add a ContributionHistory object
                contribution_in_db_dict = get_dictionary_from_model(contribution_in_db)

                if {k:v for k,v in contribution_in_db_dict.iteritems() if k != "date"} == {k:v for k,v in row.iteritems() if k != "date"}:
                    print "\tNo changes found in row %d of %s" % (idx, filepath)
                    ContributionHistory.create(date=row['date'], cycle=row['cycle'], sub_id=row['sub_id'])
                # If it has been modified, create a new object and give the new object a contribution history
                else:
                    print "\tDetected change in row %d of %s" % (idx, filepath)
                    ContributionChanges.create(**contribution_in_db_dict)
                    Contribution.update(**row)
                    ContributionHistory.create(date=row['date'], cycle=row['cycle'], sub_id=row['sub_id'])

# if __name__ == '__main__':
#     filepaths = [
#         "data/FEC 2014 2.17.2014/itcont.txt",
#         "data/FEC 2014 3.22.2015/itcont.txt",
#         "data/FEC 2014 9.14.2014/itcont.txt"
#     ]

#     for filepath in filepaths:
#         if not ingested(filepath):
#             ingest(filepath)

