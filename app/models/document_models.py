from datetime import datetime

from peewee import Model, CharField, TextField, DateTimeField, IntegerField

from app.db.database import database_instance


class Document(Model):
    id = IntegerField(primary_key=True)
    file_name = CharField(max_length=100)
    file_type = CharField(max_length=10)
    upload_timestamp = DateTimeField(default=datetime.now)
    parsed_text = TextField(null=True)

    class Meta:
        database = database_instance.database  # Set the database attribute
        table_name = 'documents'