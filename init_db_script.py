import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to PostgreSQL database (update the connection parameters as needed)
conn = psycopg2.connect(
    dbname='daiky_document_service',
    user=os.getenv('USER_NAME'),
    password=os.getenv('USER_PASSWORD'),
    host='localhost',
    port='5432'
)

# Create a cursor object
cur = conn.cursor()

# Drop tables if they exist
cur.execute('DROP TABLE IF EXISTS documents;')

# Create the users table
cur.execute('''
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(100) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    upload_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    parsed_text TEXT
);
''')

# Commit changes and close the connection
conn.commit()
cur.close()
conn.close()
