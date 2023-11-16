import extractor_functions

db_select = '2'

answer = input("do you wish to upload the following : dim_products ?")
if answer == 'y':
    extractor_functions.extract_products_table()
else:
    pass

answer = input("do you wish to upload the following : orders_table ?")
if answer == 'y':
    extractor_functions.extract_orders_table()
else:
    pass

answer = input("do you wish to upload the following : dim_store_details ?")
if answer == 'y':
    extractor_functions.extract_stores_table()
else:
    pass

answer = input("do you wish to upload the following : dim_users ?")
if answer == 'y':
    extractor_functions.extract_users_table()
else:
    pass

answer = input("do you wish to upload the following : dim_date_times ?")
if answer == 'y':
    extractor_functions.extract_date_table()
else:
    pass

answer = input("do you wish to upload the following : dim_card_details ?")
if answer == 'y':
    extractor_functions.extract_card_table(db_select)
else:
    pass