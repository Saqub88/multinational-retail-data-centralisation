import pandas as pd
import tabula
import requests
import boto3

class DataExtractor:
    def __init__(self):
        self.pd_table = None
        self.card_details_table = None
        self.key = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
        self.number_of_stores_api_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        self.stores_data_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/"
        self.number_of_stores = None
        self.stores_table = None
        self.products = None

    def read_rds_table(self, db_engine, table_name):
        from sqlalchemy import text
        with db_engine.engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name}"))
            self.pd_table = pd.DataFrame(result)
    
    def read_card_details(self, card_details_file):
        card_tables = tabula.read_pdf(card_details_file, pages='all')
        full_data = pd.DataFrame(columns=card_tables[0].columns)
        for x in range(0,len(card_tables)):
            full_data = pd.concat([full_data, card_tables[x]], ignore_index=True)
        self.card_details_table = full_data

    def list_number_of_stores(self, store_numbers_endpoint, header_key):
        response = requests.get(store_numbers_endpoint, headers=header_key)
        store_numbers = response.json()
        self.number_of_stores = store_numbers['number_stores']

    def retrieve_stores_data(self, stores_data_endpoint, header_key):
        table = {}
        for x in range(0,self.number_of_stores):
            response1 = requests.get(f"{stores_data_endpoint}{x}", headers=header_key)
            table[x] = response1.json()
            self.stores_table = pd.DataFrame.from_dict(table, orient='index')

    def extract_from_s3(self, bucket_name, object_name, file_name):
        client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
        client._request_signer.sign = (lambda *args, **kwargs: None)
        client.download_file(bucket_name, object_name, file_name)
        self.products = file_name
        
# working.