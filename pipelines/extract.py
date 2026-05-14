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

def extract_rows(filepath: str, filename: str) -> tuple[pd.DataFrame, int]:
    file_data = pd.read_csv(filepath, header=1)

    if file_data.columns is not ['name', 'year', 'count']:
        file_data = pd.read_csv(filepath, header=None, names=['name', 'year', 'count'])

        #todo: make loop logic for checking the header, if unable to get the header, mark it in the logger

    year = int(filename[-4:])

    return (file_data, year)

print(extract())
