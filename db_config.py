from peewee import (BooleanField, CharField, DateTimeField, IntegerField,
                    Model, SqliteDatabase)

db = SqliteDatabase("ActivationCodeData.db")

class ActivationCodeData(Model):
    code = CharField(primary_key=True, unique=True)
    code_type = IntegerField()
    used = BooleanField()
    use_time = DateTimeField(null=True)

    class Meta:
        database = db