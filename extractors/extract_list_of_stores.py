import yaml
import database_utils
import data_extraction
import data_cleaning


extraction = data_extraction.DataExtractor()

with open('db_key.yaml', 'r') as file:
    db_key = yaml.safe_load(file)

extraction.list_number_of_stores(extraction.number_of_stores_api_endpoint, db_key)
extraction.retrieve_stores_data(extraction.stores_data_endpoint, db_key)
stores_raw_data = extraction.stores_table

cleaner = data_cleaning.DataCleaning(stores_raw_data)

cleaner.clean_store_data()
store_data_cleaned = cleaner.clean_data


database_key = database_utils.DatabaseConnector()

#database_key.upload_to_db(store_data_cleaned, 'dim_store_details')

#database_key.upload_to_sqlite(store_data_cleaned, 'dim_store_details')