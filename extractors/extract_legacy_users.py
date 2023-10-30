import database_utils
import data_extraction
import data_cleaning

database_key = database_utils.DatabaseConnector()
database_key.read_db_creds('db_creds.yaml')
database_key.init_db_engine()
database_key.list_db_tables()

extraction = data_extraction.DataExtractor()
extraction.read_rds_table(database_key.engine, 'legacy_users')
legacy_users_raw_data = extraction.pd_table
cleaner = data_cleaning.DataCleaning(legacy_users_raw_data)
cleaner.clean_user_data()
legacy_users_cleaned = cleaner.clean_data
#database_key.upload_to_db(legacy_users_cleaned, 'dim_users')

#database_key.upload_to_sqlite(legacy_users_cleaned, 'dim_users')