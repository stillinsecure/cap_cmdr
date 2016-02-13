from peewee import *

database = SqliteDatabase('data')

class BaseModel(Model):
    class Meta:
        database = database

class Request(BaseModel):
    id = PrimaryKeyField()
    type = IntegerField()
    query = TextField()
    ip = IntegerField(null=True)
    mac = IntegerField()
    sub_type = IntegerField()
    captured = DateTimeField()

