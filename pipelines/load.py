import pandas as pd
from psycopg2.extensions import connection as Connection, cursor as Cursor
from psycopg2 import Error, ProgrammingError
from utils.logger import get_logger

logger = get_logger(__name__)

def load(cleaned: pd.DataFrame, conn: Connection, year: int):
    cur = conn.cursor()
    failed_rows = 0
    try:
        for _, row in cleaned.iterrows():
            try:
                row_id = load_names(row[['name', 'gender']], cur)
                load_details(row_id, row['count'], cur, year)
            except Exception as e:
                logger.warning(f'Skipping row {row['name']}: {e}')
                failed_rows += 1
                continue
        conn.commit()
        logger.info(f'Successfully loaded batch for year {year} | Failed rows: {failed_rows}')
    except Exception as e:
        conn.rollback()
        logger.error(f'Failed to load batch: {e}')
        raise
    finally:
        cur.close()

    return

def load_names(names_content: pd.DataFrame, cur: Cursor) -> tuple[int]:
    result = None
    LOAD_QUERY = '''
        INSERT INTO NAMES
        (name, gender)
        VALUES (%s, %s)
        ON CONFLICT (name, gender) DO NOTHING
        RETURNING name_id
    '''

    GET_ID_QUERY = '''
    SELECT name_id FROM NAMES
    WHERE name = %s AND gender = %s
    '''
    cur.execute(LOAD_QUERY, (names_content['name'], names_content['gender']))

    result = cur.fetchone()

    if result is None:
        cur.execute(GET_ID_QUERY, (names_content['name'], names_content['gender']))
        result = cur.fetchone()

    return result

def load_details(name_id: str, count: int, cur: Cursor, year: int):
    LOAD_QUERY = '''
        INSERT INTO DETAILS
        (name_id, year, count)
        VALUES (%s, %s, %s)
        ON CONFLICT (name_id, year) DO UPDATE SET
            count = EXCLUDED.count
            updated_at = NOW()
    '''
    cur.execute(LOAD_QUERY, (name_id, year, count))
    return