import database_utils
import data_extraction
import data_cleaning

bucket_name = 'data-handling-public'
object_name = 'date_details.json'
file_name = 'date_details.json'

extraction = data_extraction.DataExtractor()
extraction.extract_from_s3(bucket_name, object_name, file_name)
date_details_raw = extraction.products

cleaner = data_cleaning.DataCleaning(date_details_raw)
cleaner.clean_date_details()
date_details_clean = cleaner.clean_data

database_key = database_utils.DatabaseConnector()
database_key.upload_to_db(date_details_clean, 'dim_date_times')

# database_key.upload_to_sqlite(date_details_clean, 'dim_date_times')