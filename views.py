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

transaction_pgi_dict = {
	"P": "Primary",
	"G": "General",
	"O": "Other",
	"C": "Convention",
	"R": "Runoff",
	"S": "Special",
	"E": "Recount"
}

ammendment_id_dict = {
	"N": "new",
	"A": "ammendment",
	"T": "termination"
}

transaction_tp_dict = {
	"10": "Non-Federal Receipt from Persons",
	"10J": "Memo Receipt from JF Super PAC",
	"11": "Tribal Contribution",
	"11J": "Memo Receipt from JF Tribal",
	"12": "Non-Federal Other Receipt - Levin Account (L-2)",
	"13": "Inaugural Donation Accepted",
	"15": "Contribution",
	"15C": "Contribution from Candidate",
	"15E": "Earmarked Contribution",
	"15F": "Loans forgiven by Candidate",
	"15I": "Earmarked Intermediary In",
	"15J": "Memo (Filer's Percentage of Contribution Given to Join Fundraising Committee)",
	"15T": "Earmarked Intermediary Treasury In",
	"15Z": "In-Kind Contribution Received from Registered Filer",
	"16C": "Loans Received from the Candidate",
	"16F": "Loans Received from Banks",
	"16G": "Loan from Individual",
	"16H": "Loan from from Registered Filers",
	"16J": "Loan Repayments from Individual",
	"16K": "Loan Repayments from from Registered Filer",
	"16L": "Loan Repayments Received from Unregistered Entity",
	"16R": "Loans Received from Registered Filers",
	"16U": "Loan Received from Unregistered Entity",
	"17R": "Contribution Refund Received from Registered Entity",
	"17U": "Refunds/Rebates/Returns Received from Unregistered Entity",
	"17Y": "Refunds/Rebates/Returns from Individual or Corporation",
	"17Z": "Refunds/Rebates/Returns from Candidate or Committee",
	"18G": "Transfer In Affiliated",
	"18H": "Honorarium Received",
	"18J": "Memo (Filer's Percentage of Contribution Given to Join Fundraising Committee)",
	"18K": "Contribution Received from Registered Filer",
	"18L": "Bundled Contribution",
	"18S": "Receipts from Secretary of State",
	"18U": "Contribution Received from Unregistered Committee",
	"19": "Electioneering Communication Donation Received",
	"19J": "Memo (Electioneering Communication Percentage of Donation Given to Join Fundraising Committee)",
	"20": "Disbursement - Exempt from Limits",
	"20A": "Non-Federal Disbursement - Levin Account (L-4A) Voter Registration",
	"20B": "Non-Federal Disbursement - Levin Account (L-4B) Voter Identification",
	"20C": "Loan Repayments Made to Candidate",
	"20D": "Non-Federal Disbursement - Levin Account (L-4D) Generic Campaign",
	"20F": "Loan Repayments Made to Banks",
	"20G": "Loan Repayments Made to Individual",
	"20R": "Loan Repayments Made to Registered Filer",
	"20V": "Non-Federal Disbursement - Levin Account (L-4C) Get Out The Vote",
	"20Y": "Non-Federal Refund",
	"21Y":	"Tribal Refund",
	"22G":	"Loan to Individual",
	"22H":	"Loan to Candidate or Committee",
	"22J":	"Loan Repayment to Individual",
	"22K":	"Loan Repayment to Candidate or Committee",
	"22L":	"Loan Repayment to Bank",
	"22R":	"Contribution Refund to Unregistered Entity",
	"22U":	"Loan Repaid to Unregistered Entity",
	"22X":	"Loan Made to Unregistered Entity",
	"22Y":	"Contribution Refund to Individual",
	"22Z":	"Contribution Refund to Candidate or Committee",
	"23Y":	"Inaugural Donation Refund",
	"24A":	"Independent Expenditure Against",
	"24C":	"Coordinated Expenditure",
	"24E":	"Independent Expenditure For",
	"24F":	"Communication Cost for Candidate (C7)",
	"24G":	"Transfer Out Affiliated",
	"24H":	"Honorarium to Candidate",
	"24I":	"Earmarked Intermediary Out",
	"24K":	"Contribution Made to Non-Affiliated",
	"24N":	"Communication Cost Against Candidate (C7)",
	"24P":	"Contribution Made to Possible Candidate",
	"24R":	"Election Recount Disbursement",
	"24T":	"Earmarked Intermediary Treasury Out",
	"24U":	"Contribution Made to Unregistered Entity",
	"24Z":	"In-Kind Contribution Made to Registered Filer",
	"28L":	"Refund of Bundled Contribution",
	"29":   "Electioneering Communication Disbursement or Obligation"
}

report_type_dict = {
	"12C": "PRE-CONVENTION",
	"12G": "PRE-GENERAL",
	"12P": "PRE-PRIMARY",
	"12R": "PRE-RUN-OFF",
	"12S": "PRE-SPECIAL",
	"30D": "POST-ELECTION",
	"30G": "POST-GENERAL",
	"30P": "POST-PRIMARY",
	"30R": "POST-RUN-OFF",
	"30S": "POST-SPECIAL",
	"60D": "POST-CONVENTION",
	"ADJ": "COMP ADJUST AMEND",
	"CA": "COMPREHENSIVE AMEND",
	"M10": "OCTOBER MONTHLY",
	"M11": "NOVEMBER MONTHLY",
	"M12": "DECEMBER MONTHLY",
	"M2": "FEBRUARY MONTHLY",
	"M3": "MARCH MONTHLY",
	"M4": "APRIL MONTHLY",
	"M5": "MAY MONTHLY",
	"M6": "JUNE MONTHLY",
	"M7": "JULY MONTHLY",
	"M8": "AUGUST MONTHLY",
	"M9": "SEPTEMBER MONTHLY",
	"MY": "MID-YEAR REPORT",
	"Q1": "APRIL QUARTERLY",
	"Q2": "JULY QUARTERLY",
	"Q3": "OCTOBER QUARTERLY",
	"TER": "TERMINATION REPORT",
	"YE": "YEAR-END",
	"90S": "POST INAUGURAL SUPPLEMENT",
	"90D": "POST INAUGURAL",
	"48H": "48 HOUR NOTIFICATION",
	"24H": "24 HOUR NOTIFICATION"
}

@app.route('/')
def hello():
	before = dateparse(request.args.get('before')).date()
	after = dateparse(request.args.get('after')).date()

	ret = []

	for contrib in ContributionChanges.select().where(ContributionChanges.date == before):
		before_contrib_dict = get_dictionary_from_model(contrib)
		after_contrib_dict = get_dictionary_from_model(Contribution.get(sub_id=contrib.sub_id).get_on_date(after))

		before_contrib_dict.pop('id')
		before_contrib_dict.pop('contribution')
		after_contrib_dict.pop('id')

		after_contrib_dict['transaction_pgi'] = transaction_pgi_dict[after_contrib_dict['transaction_pgi']] if after_contrib_dict['transaction_pgi'] else None
		before_contrib_dict['transaction_pgi'] = transaction_pgi_dict[before_contrib_dict['transaction_pgi']] if before_contrib_dict['transaction_pgi'] else None

		after_contrib_dict['ammendment_id'] = ammendment_id_dict[after_contrib_dict['ammendment_id']] if after_contrib_dict['ammendment_id'] else None
		before_contrib_dict['ammendment_id'] = ammendment_id_dict[before_contrib_dict['ammendment_id']] if before_contrib_dict['ammendment_id'] else None

		after_contrib_dict['transaction_tp'] = transaction_tp_dict[after_contrib_dict['transaction_tp']] if after_contrib_dict['transaction_tp'] else None
		before_contrib_dict['transaction_tp'] = transaction_tp_dict[before_contrib_dict['transaction_tp']] if before_contrib_dict['transaction_tp'] else None

		after_contrib_dict['report_type'] = report_type_dict[after_contrib_dict['report_type']] if after_contrib_dict['report_type'] else None
		before_contrib_dict['report_type'] = report_type_dict[before_contrib_dict['report_type']] if before_contrib_dict['report_type'] else None
		# report_type_dict

		ret.append({
			"before": before_contrib_dict,
			"after": after_contrib_dict,
			"changes": list(set([x[1][0][0] for x in diff(before_contrib_dict, after_contrib_dict).diffs if x[0] not in ["equal", "context_end_container"] and x[1][0][0] not in ['contribution', 'date', 'id']]))
		})

	before_sub_ids = set([x.sub_id for x in ContributionHistory.select().where(ContributionHistory.date == before)])
	after_sub_ids = set([x.sub_id for x in ContributionHistory.select().where(ContributionHistory.date == after)])

	for sub_id in (before_sub_ids - after_sub_ids):
		ret.append({
			"before": get_dictionary_from_model(Contribution.get(sub_id=sub_id)),
			"after": None,
			"changes": None
		})

	return render_template('diff.html', ret=ret, before=before, after=after)
	# return json.dumps(ret, default=date_handler)
