import database_utils
import data_extraction
import data_cleaning

database_key = database_utils.DatabaseConnector()
extraction = data_extraction.DataExtractor()

extraction.read_card_details('card_details.pdf')
card_details_raw = extraction.card_details_table
cleaner = data_cleaning.DataCleaning(card_details_raw)
cleaner.clean_card_details()

card_details_cleaned = cleaner.clean_data
database_key.upload_to_db(card_details_cleaned, 'dim_card_details')

# database_key.upload_to_sqlite(card_details_cleaned, 'dim_card_details')
