""" Docstring for M2_simple_extractor.
This file is intended to simplify the process of uploading a table to 1 of the 
2 default databases. The first being the postgresql based one and the other for
use with a sqlite one. The code will offer a key of the tables as well as the 
key for the databases to which they can be uploaded.
There will be prompts along the process to guide the user through
"""

import extractor_functions
import json

print("Welcome!")
print("This script will upload your chosen tables to the selected database")
print("The following are the tables with thier respective key")

with open("keys/table_key.json", "r") as file_1:
    table_key = json.load(file_1)
for keys, values in table_key.items():
    print(f"{keys} - {values}")

table_request = input("Please list numerical keys of tables to upload : ")

with open("keys/database_key.json", "r") as file_2:
    database_key = json.load(file_2)
for keys, values in database_key.items():
    print(f"{keys} - {values}")

db_request = input("Please list numerical keys of database to upload to : ")


def filter(input_str):
    """
    Will clean the input list to include valid characters.

    Function will take in a string sequence and iterate through the characeters
    to remove all non-numeric characters and duplicates.

    :param input_str: string sequence from a users input
    :return: List of numerical character only with no duplicates
    """
    output_set = set()
    for x in range(0, len(input_str)):
        if input_str[x].isnumeric() == True:
            output_set.add((input_str[x]))
    return list(output_set)


requested_table_list = filter(table_request)
requested_db_list = filter(db_request)
print(requested_table_list)
print(requested_db_list)

if "5" in requested_table_list or "0" in requested_table_list:
    extractor_functions.extract_products_table(requested_db_list)
if "6" in requested_table_list or "0" in requested_table_list:
    extractor_functions.extract_orders_table(requested_db_list)
if "4" in requested_table_list or "0" in requested_table_list:
    extractor_functions.extract_stores_table(requested_db_list)
if "3" in requested_table_list or "0" in requested_table_list:
    extractor_functions.extract_users_table(requested_db_list)
if "2" in requested_table_list or "0" in requested_table_list:
    extractor_functions.extract_date_table(requested_db_list)
if "1" in requested_table_list or "0" in requested_table_list:
    extractor_functions.extract_card_table(requested_db_list)
