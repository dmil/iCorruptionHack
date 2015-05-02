from app import app
from models import File, Contribution, ContributionChanges, ContributionHistory

from flask_peewee.utils import get_dictionary_from_model

from flask import request

# from bson import json_util
import json

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

from dateutil.parser import parse as dateparse

@app.route('/summary')
def summary():
    text = '<h1>Database Summary</h1>\n'
    file1 = File.get(id=1)
    file2 = File.get(id=2)
    file3 = File.get(id=3)

    text += '<h2>' + file1.name + '</h2>\n'
    text += '<h2>' + file2.name + '</h2>\n'
    text += '<h2>' + file3.name + '</h2>\n'

    return text

@app.route('/')
def hello():
	before = dateparse(request.args.get('before')).date()
	after = dateparse(request.args.get('after')).date()

	ret = []

	for contrib in ContributionChanges.select().where(ContributionChanges.date == before):
		ret.append(
			{
				"before": get_dictionary_from_model(contrib),
				"after": get_dictionary_from_model(Contribution.get(sub_id=contrib.sub_id).get_on_date(after))
			}
		)

	return json.dumps(ret, default=date_handler)
