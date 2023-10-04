import database_utils
import data_extraction
import data_cleaning

database_key = database_utils.DatabaseConnector()
database_key.read_db_creds('db_creds.yaml')
database_key.init_db_engine()
database_key.list_db_tables()
print(database_key.list_tables)
# as intended will return the following : ['legacy_store_details', 'legacy_users', 'orders_table']

extraction = data_extraction.DataExtractor()
extraction.read_rds_table(database_key.engine, 'orders_table')
orders_table_raw = extraction.pd_table
cleaner = data_cleaning.DataCleaning(orders_table_raw)
cleaner.clean_orders_data()
orders_table_clean = cleaner.clean_data
database_key.upload_to_db(orders_table_clean, 'orders_table')

# database_key.upload_to_sqlite(orders_table_clean, 'orders_table')