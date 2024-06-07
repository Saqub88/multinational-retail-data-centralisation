import data_cleaning
import data_extraction
import database_utils
import yaml

database_key = database_utils.DatabaseConnector()
extractor = data_extraction.DataExtractor()


def retrieve_rds_tables():
    if database_key.list_tables == None:
        database_key.read_db_creds("db_creds.yaml")
        database_key.init_db_engine()
        database_key.list_db_tables()


def db_select(db_choice, cleaned_dataframe, db_name):
    if "1" in db_choice or "0" in db_choice:
        database_key.upload_to_db(cleaned_dataframe, db_name)
    if "2" in db_choice or "0" in db_choice:
        database_key.upload_to_sqlite(cleaned_dataframe, db_name)


def extract_card_table(select_database):
    extractor.read_card_details("raw_data/card_details.pdf")
    card_data_cleaner = data_cleaning.Card_data_cleaning(extractor.raw_card_data)
    card_data_cleaner.clean_card_details()
    db_select(select_database, card_data_cleaner.clean_data, "dim_card_details")


def extract_date_table(select_database):
    s3_object_name = "date_details.json"
    output_file_name = "raw_data/raw_date_details.json"
    extractor.extract_from_s3(s3_object_name, output_file_name)
    date_data_cleaner = data_cleaning.Date_data_cleaning(output_file_name)
    date_data_cleaner.clean_date_details()
    db_select(select_database, date_data_cleaner.clean_data, "dim_date_times")


def extract_users_table(select_database):
    retrieve_rds_tables()
    extractor.read_rds_table(database_key.engine, "legacy_users")
    users_data_cleaner = data_cleaning.User_data_cleaning(extractor.raw_dataframe)
    users_data_cleaner.clean_user_data()
    db_select(select_database, users_data_cleaner.clean_data, "dim_users")


def extract_stores_table(select_database):
    with open("db_key.yaml", "r") as file:
        db_key = yaml.safe_load(file)
    extractor.list_number_of_stores(extractor.number_of_stores_api_endpoint, db_key)
    extractor.retrieve_stores_data(extractor.stores_data_endpoint, db_key)
    stores_data_cleaner = data_cleaning.Store_data_cleaning(extractor.raw_stores_data)
    stores_data_cleaner.clean_store_data()
    db_select(select_database, stores_data_cleaner.clean_data, "dim_store_details")


def extract_orders_table(select_database):
    retrieve_rds_tables()
    extractor.read_rds_table(database_key.engine, "orders_table")
    orders_data_cleaner = data_cleaning.Order_data_cleaning(extractor.raw_dataframe)
    orders_data_cleaner.clean_orders_data()
    db_select(select_database, orders_data_cleaner.clean_data, "orders_table")


def extract_products_table(select_database):
    s3_object_name = "products.csv"
    output_file_name = "raw_data/raw_products.csv"
    extractor.extract_from_s3(s3_object_name, output_file_name)
    products_data_cleaner = data_cleaning.Product_data_cleaning(output_file_name)
    products_data_cleaner.clean_products_data()
    db_select(select_database, products_data_cleaner.clean_data, "dim_products")