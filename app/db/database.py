# app/db/database.py
import os
from peewee import PostgresqlDatabase
from dotenv import load_dotenv, dotenv_values

load_dotenv()

class Database:

    def __init__(self, database_url: str):
        self.database = PostgresqlDatabase(database_url)

    def connect(self):
        self.database.connect()

    def close(self):
        if not self.database.is_closed():
            self.database.close()

    def create_tables(self, models):
        """Create tables in the database."""
        with self.database:
            self.database.create_tables(models, safe=True)

db_url = f"{os.getenv('DATABASE_PUBLIC_URL')}"
database_instance = Database(db_url)