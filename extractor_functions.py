import data_cleaning
import data_extraction
import database_utils
import yaml

database_key = database_utils.DatabaseConnector()

def db_select(db_choice, cleaned_dataframe, db_name):
    if db_choice == '1' or '0':
        database_key.upload_to_db(cleaned_dataframe, db_name)
    elif db_choice == '2' or '0':
        print('choice 2 accepted')
        database_key.upload_to_sqlite(cleaned_dataframe, db_name)
    else:
        print("Invalid selection, Please run file again")

def extract_card_table(select_database):
    database_key = database_utils.DatabaseConnector()
    extraction = data_extraction.DataExtractor()

    extraction.read_card_details('card_details.pdf')
    card_details_raw = extraction.card_details_table
    cleaner = data_cleaning.Card_data_cleaning(card_details_raw)
    cleaner.clean_card_details()

    card_details_cleaned = cleaner.clean_data

    db_select(select_database, card_details_cleaned, 'dim_card_details')


def extract_date_table():
    bucket_name = 'data-handling-public'
    object_name = 'date_details.json'
    file_name = 'date_details.json'

    extraction = data_extraction.DataExtractor()
    extraction.extract_from_s3(bucket_name, object_name, file_name)
    date_details_raw = extraction.products

    cleaner = data_cleaning.Date_data_cleaning(date_details_raw)
    cleaner.clean_date_details()
    date_details_clean = cleaner.clean_data

    database_key = database_utils.DatabaseConnector()

    select_database = input("1 for postgresql, 2 for sqlite")
    if select_database == '1':
        database_key.upload_to_db(date_details_clean, 'dim_date_times')
    elif select_database == '2':
        database_key.upload_to_sqlite(date_details_clean, 'dim_date_times')
    else:
        print("Invalid selection, Please run file again")

def extract_users_table():
    database_key = database_utils.DatabaseConnector()
    database_key.read_db_creds('db_creds.yaml')
    database_key.init_db_engine()
    database_key.list_db_tables()

    extraction = data_extraction.DataExtractor()
    extraction.read_rds_table(database_key.engine, 'legacy_users')
    legacy_users_raw_data = extraction.pd_table
    cleaner = data_cleaning.User_data_cleaning(legacy_users_raw_data)
    cleaner.clean_user_data()
    legacy_users_cleaned = cleaner.clean_data

    select_database = input("1 for postgresql, 2 for sqlite")
    if select_database == '1':
        database_key.upload_to_db(legacy_users_cleaned, 'dim_users')
    elif select_database == '2':
        database_key.upload_to_sqlite(legacy_users_cleaned, 'dim_users')
    else:
        print("Invalid selection, Please run file again")

def extract_stores_table():
    with open("db_key.yaml", "r") as file:
        db_key = yaml.safe_load(file)

    extraction = data_extraction.DataExtractor()
    extraction.list_number_of_stores(extraction.number_of_stores_api_endpoint, db_key)
    extraction.retrieve_stores_data(extraction.stores_data_endpoint, db_key)
    stores_raw_data = extraction.stores_table

    cleaner = data_cleaning.Store_data_cleaning(stores_raw_data)

    cleaner.clean_store_data()
    store_data_cleaned = cleaner.clean_data


    database_key = database_utils.DatabaseConnector()

    select_database = input("1 for postgresql, 2 for sqlite")
    if select_database == '1':
        database_key.upload_to_db(store_data_cleaned, 'dim_store_details')
    elif select_database == '2':
        database_key.upload_to_sqlite(store_data_cleaned, 'dim_store_details')
    else:
        print("Invalid selection, Please run file again")

def extract_orders_table():
    database_key = database_utils.DatabaseConnector()
    database_key.read_db_creds('db_creds.yaml')
    database_key.init_db_engine()
    database_key.list_db_tables()
    print(database_key.list_tables)
    # as intended will return the following : ['legacy_store_details', 'legacy_users', 'orders_table']

    extraction = data_extraction.DataExtractor()
    extraction.read_rds_table(database_key.engine, 'orders_table')
    orders_table_raw = extraction.pd_table
    cleaner = data_cleaning.Order_data_cleaning(orders_table_raw)
    cleaner.clean_orders_data()
    orders_table_clean = cleaner.clean_data

    select_database = input("1 for postgresql, 2 for sqlite")
    if select_database == '1':
        database_key.upload_to_db(orders_table_clean, 'orders_table')
    elif select_database == '2':
        database_key.upload_to_sqlite(orders_table_clean, 'orders_table')
    else:
        print("Invalid selection, Please run file again")

def extract_products_table():
    bucket_name = 'data-handling-public'
    object_name = 'products.csv'
    file_name = 'products.csv'

    extraction = data_extraction.DataExtractor()
    extraction.extract_from_s3(bucket_name, object_name, file_name)
    products_raw = extraction.products

    cleaner = data_cleaning.Product_data_cleaning(products_raw)
    cleaner.clean_products_data()
    products_clean = cleaner.clean_data

    database_key = database_utils.DatabaseConnector()

    select_database = input("1 for postgresql, 2 for sqlite")
    if select_database == '1':
        database_key.upload_to_db(products_clean, "dim_products")
    elif select_database == '2':
        database_key.upload_to_sqlite(products_clean, "dim_products")
    else:
        print("Invalid selection, Please run file again")

