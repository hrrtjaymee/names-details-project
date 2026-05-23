import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)


def transform(data_records: pd.DataFrame) -> tuple[pd.DataFrame]:

   logger.info(f'Transforming batch')
   
   data_records = data_records.apply(checking_gender, axis=1).dropna().reset_index(drop=True)
   try:
      data_records['count'] = data_records['count'].astype(int)
   except ValueError as e:
      logger.warning(f'Batch contains invalid count value: {e}')
      data_records = data_records.apply(checking_count, axis=1).dropna().reset_index(drop=True)
   
   data_records['name'] = data_records['name'].str.capitalize()

   data_records = data_records.drop_duplicates(subset=['name', 'gender']).reset_index(drop=True)

   logger.info(f'Finished transforming batch')
   return data_records

def checking_gender(record):
   if record['gender'].lower() in ['f', 'female']:
      record['gender'] = 'F'
   elif record['gender'].lower() == 'm' or record['gender'].lower() == 'male':
      record['gender'] = 'M'
   else:
      logger.warning(f'Invalid gender value: {record['gender']} for {record['name']}')
      record = pd.NA

   return record

def checking_count(record):
   try:
      record['count'] = record['count'].astype(int)
   except ValueError as e:
      logger.warning(f'Invalid count value found for {record['name']}: {e}')
      record['count'] = pd.NA

   if record['count'] < 0:
      logger.warning(f'Negative number for count is invalid')
      record['count'] = pd.NA
   return record