import database_utils
import data_extraction
import data_cleaning

bucket_name = 'data-handling-public'
object_name = 'products.csv'
file_name = 'products.csv'

extraction = data_extraction.DataExtractor()
extraction.extract_from_s3(bucket_name, object_name, file_name)
products_raw = extraction.products

cleaner = data_cleaning.DataCleaning(products_raw)
cleaner.clean_products_data()
products_clean = cleaner.clean_data

database_key = database_utils.DatabaseConnector()
#database_key.upload_to_db(products_clean, 'dim_products')

#database_key.upload_to_sqlite(products_clean, 'dim_products')