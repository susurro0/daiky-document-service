import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Parameters
DB_NAME = "daiky"
DB_USER = os.getenv("USER_NAME")
DB_PASSWORD = os.getenv("USER_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"

def create_database_if_not_exists():
    """Creates the database if it doesn't already exist."""
    try:
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(
            dbname="postgres",  # Default DB
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True  # Enable auto-commit for database creation
        cursor = conn.cursor()

        # Check if the database already exists
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"),
            [DB_NAME]
        )
        exists = cursor.fetchone()

        if not exists:
            # Create the database
            print(f"Database '{DB_NAME}' does not exist. Creating it...")
            cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(DB_NAME)))
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists. Skipping creation.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error while creating database: {e}")

def initialize_schema():
    """Initializes the database schema."""
    try:
        # Connect to the target database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Drop tables if they exist
        cursor.execute("DROP TABLE IF EXISTS documents;")

        # Create the documents table
        cursor.execute('''
        CREATE TABLE documents (
            id SERIAL PRIMARY KEY,
            file_name VARCHAR(100) NOT NULL,
            file_type VARCHAR(100) NOT NULL,
            upload_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            parsed_text TEXT
        );
        ''')
        print("Schema initialized successfully.")

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error during schema initialization: {e}")

if __name__ == "__main__":
    # Create the database if it doesn't exist
    create_database_if_not_exists()

    # Initialize the schema
    initialize_schema()
