import os
import sys
import psycopg2
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)


load_dotenv(dotenv_path=os.path.join(dirname, '..', '.env'))


DATABASE_URL = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
except psycopg2.OperationalError:
    sys.exit(
        """Unable to connect to a database!
        Make sure that you created a .env-file with the parameter DATABASE_URL""")


def get_db_connection():
    return conn
