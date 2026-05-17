from database import get_connection
from pipelines.extract import extract, extract_rows
from pipelines.transform import transform
from pipelines.load import load
from utils.logger import get_logger

logger = get_logger(__name__)
BATCH_SIZE = 40

def main():
    logger.info('Starting pipeline')

    try:
        connection = get_connection()
    except Exception as e:
        logger.critical(f'Failed databse connection: {e}')
        return
    
    try:
        files = extract()
    except FileNotFoundError as e:
        logger.critical(f'Extraction failed: {e}')
        return 
    
    for file in files:
        try:
            data_records, year = extract_rows(file)

            if data_records.empty and year == 0:
                logger.info(f'Data record empty; moving to next file')
                continue

            BATCH_NUM = 1
            start = 0
            end = BATCH_SIZE

            if len(data_records) >= BATCH_SIZE:
                while start < len(data_records):
                    logger.info(f'Processing batch number {BATCH_NUM}')
                    transformed = transform(data_records.iloc[start:end])
                    load(transformed, connection, year)
                    BATCH_NUM += 1
                    start = end
                    end += BATCH_SIZE
            else:
                try:
                    logger.info(f'Processing all records')
                    transformed = transform(data_records.iloc[start:end])
                    load(transformed, connection)
                except Exception as e:
                    logger.warning(f'Failed to load batch {BATCH_NUM} from {file}, skipping')
                    continue
        except Exception as e:
            logger.error(f'Failed to process file {file}')
            continue
        logger.info(f'Finished processing file {file}')
        
if __name__ == '__main__':
    main()