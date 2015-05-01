import json
import requests

from app import db

from app import db

from models import File, CampaignAndComitteeSummary

from flask_peewee.utils import get_dictionary_from_model

from dateutil.parser import parse as dateparse

# import the demo key from env vars
import os


DEMO_KEY=os.environ['API_KEY']
API_URL='http://api.open.fec.gov/v1'

# important fields
name_converter = {
        'committee_id': 'com_id',
        'total_contributions': 'tot_con',
        'total_recipts_period': 'tot_rec',
        'total_disbursements_period': 'tot_dis',
        'report_type': 'rep_typ',
        'cash_on_hand_end_period': 'cas_on_han_clo_of_per',
        'coverage_end_date': 'cov_end_dat'
}

def check_report_data(test_committees):
    query_params = {
            'api_key': DEMO_KEY,
    }

    records = []
    for com in test_committees:
        print(com)
        url = API_URL + '/committee/' + com + '/reports'
        response = requests.get(url, params=query_params)
        response = response.json()

        if response['results'] == []:
            print("\nRecords for committee %s MISSING in bulk data\n" % (committee_id))

        for record in response['results']:
            for key in record:
                named_record = {}
                if key in name_converter:
                    named_record[name_converter[key]] = record[key]
            # might need to add variables that we aren't checking
                print(named_record)
                records.append(named_record)

    CampaignAndComitteeSummary.insert_many(records).execute()

# replace this with
test_committees = ['C00239533', ]
check_report_data(test_committees)


