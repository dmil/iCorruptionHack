from app import app
from models import File, Contribution, ContributionChanges, ContributionHistory

from flask_peewee.utils import get_dictionary_from_model

from flask import request, render_template

import json

from datadiff import diff

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

def dumps(x, **args):
	return json.dumps(x, default=date_handler, **args)

@app.route('/')
def hello():
	before = dateparse(request.args.get('before')).date()
	after = dateparse(request.args.get('after')).date()

	ret = []

	for contrib in ContributionChanges.select().where(ContributionChanges.date == before):
		before_contrib_dict = get_dictionary_from_model(contrib)
		after_contrib_dict = get_dictionary_from_model(Contribution.get(sub_id=contrib.sub_id).get_on_date(after))

		ret.append(
			{
				"before": before_contrib_dict,
				"after": after_contrib_dict,
				"changes": [
					x for x in diff(before_contrib_dict, after_contrib_dict).diffs if x[0] not in ['equal', 'context_end_container'] and x[1][0][0] not in ['contribution', 'date', 'id']
				]
			}
		)

	return render_template('diff.html', ret=ret, dumps=dumps)
	# return json.dumps(ret, default=date_handler)
