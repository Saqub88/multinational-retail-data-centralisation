import pandas as pd
import tabula
import requests
import boto3
from sqlalchemy import text


class DataExtractor:
    def __init__(self):
        self.s3_bucket_name = "data-handling-public"
        self.number_of_stores_api_endpoint = (
            "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        )
        self.stores_data_endpoint = (
            "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/"
        )
        self.number_of_stores = None
        self.raw_stores_data = None
        self.raw_dataframe = None
        self.raw_card_data = None

    def read_rds_table(self, db_engine, table_name):
        with db_engine.engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name}"))
            self.raw_dataframe = pd.DataFrame(result)

    def read_card_details(self, card_details_file):
        card_tables = tabula.read_pdf(card_details_file, pages="all")
        full_data = pd.DataFrame(columns=card_tables[0].columns)
        for x in range(0, len(card_tables)):
            full_data = pd.concat([full_data, card_tables[x]], ignore_index=True)
        self.raw_card_data = full_data

    def list_number_of_stores(self, store_numbers_endpoint, header_key):
        response = requests.get(store_numbers_endpoint, headers=header_key)
        store_numbers = response.json()
        self.number_of_stores = store_numbers["number_stores"]

    def retrieve_stores_data(self, stores_data_endpoint, header_key):
        table = {}
        for x in range(0, self.number_of_stores):
            response1 = requests.get(f"{stores_data_endpoint}{x}", headers=header_key)
            table[x] = response1.json()
            self.raw_stores_data = pd.DataFrame.from_dict(table, orient="index")

    def extract_from_s3(self, object_name, output_file_name):
        client = boto3.client("s3", aws_access_key_id="", aws_secret_access_key="")
        client._request_signer.sign = lambda *args, **kwargs: None
        client.download_file(self.s3_bucket_name, object_name, output_file_name)
