from psycopg2 import connect
from psycopg2 import Error
from dotenv import load_dotenv
import os
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def get_connection():
    connection = None
    try:
        connection = connect(
            dbname=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT'),
        )
        logger.info(f'Successfully connected to database')
    except Error as e:
        logger.error(f'Error in database connection: {e}')
    return connection

