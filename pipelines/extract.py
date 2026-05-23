import os
import pandas as pd
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/raw')
BATCH_SIZE = 100

def extract():
    logger.info(f'Extracting files in the filepath')
    files = []

    #getting all the extractable files in the folder
    for f in os.listdir(DATA_PATH):
        if f.startswith('yob') and f.endswith('.txt'):
            files.append(f)

    ##check if data list is empty
    if not files:
        logger.error(f'No file found for extraction in {DATA_PATH}')
        raise FileNotFoundError(f'No file found for extraction in {DATA_PATH}')
    
    logger.info(f'Finished all file extraction: {len(files)} files')
    return files

def extract_rows(filename: str) -> tuple[pd.DataFrame, int]:
    logger.info(f'Extracting rows from file: {filename}')
    
    filepath = f'{DATA_PATH}/{filename}'
    file_data = None
    empty_result = (pd.DataFrame(columns=['name', 'gender', 'count']), 0)

    try:
        check = pd.read_csv(filepath, header=None)
    except pd.errors.EmptyDataError as e:
        logger.warning(f'File contains no headers nor data, skipping')
        return empty_result
    
    #checking the first row for headers
    header_check = check.iloc[0].to_list()
    
    if header_check == ['name', 'gender', 'count']:
        file_data = pd.read_csv(filepath, header=0)
        if file_data.empty:
            logger.warning(f'{filename} has headers but no data, skipping')
            return empty_result
    else:
        logger.warning(f'File {filename} has no headers')
        file_data = pd.read_csv(filepath, header=None, names=['name', 'gender', 'count'])

    
    ##retreiving year
    year = int(filename.replace('.txt', '')[-4:])
    logger.info(f'Finished extracting all {len(file_data)} rows from {filename}')
    
    return file_data, year
