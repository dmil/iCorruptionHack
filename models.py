import re
from blessings import Terminal
from peewee import *
from app import db

t = Terminal()

class BaseModel(Model):
    class Meta:
        database = db

class File(BaseModel):
    id = PrimaryKeyField()
    name = CharField(null=True, default=None)
    year = IntegerField(null=True, default=None)
    updated = DateTimeField(null=True, default=None)

    def __str__(self):
        return self.name

class ContributionBaseModel(BaseModel):
    cycle = CharField(null=False)
    comittee_id = CharField(null=True, default=None)
    ammendment_id = CharField(null=True, default=None)
    report_type = CharField(null=True, default=None)
    transaction_pgi = CharField(null=True, default=None)
    image_num = CharField(null=True, default=None)
    transaction_tp = CharField(null=True, default=None)
    entity_tp = CharField(null=True, default=None)
    name = CharField(null=True, default=None)
    city = CharField(null=True, default=None)
    state = CharField(null=True, default=None)
    zip_code = CharField(null=True, default=None)
    employer = CharField(null=True, default=None)
    occupation = CharField(null=True, default=None)
    transaction_date = DateTimeField(null=True, default=None)
    transaction_amount = FloatField(null=True, default=None)
    other_id = CharField(null=True, default=None)
    transaction_id = CharField(null=True, default=None)
    file_num = IntegerField(null=True, default=None)
    memo_cd = CharField(null=True, default=None)
    memo_text = CharField(null=True, default=None)

# Most Recent Contributions
class Contribution(BaseModel, ContributionBaseModel):
    sub_id = CharField(null=False)

    class Meta:
        primary_key = CompositeKey('cycle', 'sub_id')

# ContributionChanges
class ContributionChanges(BaseModel, ContributionBaseModel):
    sub_id = ForeignKeyField(Contribution, related_name='changes')
    date = DateField(null=False)

    class Meta:
        primary_key = CompositeKey('date', 'cycle', 'sub_id')

# ContributionHistory
class ContributionHistory(BaseModel):
    sub_id = ForeignKeyField(Contribution, related_name='history')
    date = DateField(null=False)

    class Meta:
        primary_key = CompositeKey('date', 'cycle', 'sub_id')
