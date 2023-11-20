import extractor_functions
import json

print("Welcome!\nThis script is will allow you to select the tables you wish upload to your database")
print("The following is a list of tables available to upload to your database")

with open('keys/table_key.json', 'r') as file_1:
    table_key = json.load(file_1)
file_1.close()
for keys, values in table_key.items():
    print(f"{keys} - {values}")

table_request = input("Please list tables to extract into single string :")

with open('keys/database_key.json', 'r') as file_2:
    database_key = json.load(file_2)
file_2.close()
for keys, values in database_key.items():
    print(f"{keys} - {values}")

db_request = input("which database version would you like to upload to :")

def filter(input_list):
    output_set = set()
    for x in range(0,len(input_list)):
        if input_list[x].isnumeric() == True:
            output_set.add((input_list[x]))
    return list(output_set)

requested_table_list = filter(table_request)
requested_db_list = filter(db_request)
print(requested_table_list)
print(requested_db_list)

if ('5' or '0') in requested_table_list:
    extractor_functions.extract_products_table(requested_db_list)
if ('6' or '0') in requested_table_list:
    extractor_functions.extract_orders_table(requested_db_list)
if ('4' or '0') in requested_table_list:
    extractor_functions.extract_stores_table(requested_db_list)
if ('3' or '0') in requested_table_list:
    extractor_functions.extract_users_table(requested_db_list)
if ('2' or '0') in requested_table_list:
    extractor_functions.extract_date_table(requested_db_list)
if ('1' or '0') in requested_table_list:
    extractor_functions.extract_card_table(requested_db_list)
else: pass