import os
import psycopg2
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)


load_dotenv(dotenv_path=os.path.join(dirname, '..', '.env'))


DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def get_db_connection():
    return conn





