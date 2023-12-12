import pandas as pd

class DataCleaning():
    '''
    Parent class for cleaning data
    '''
    def __init__(self, raw_data):
        '''
        :param raw_data: table of raw data extracted from source to be cleaned
        '''
        self.raw_data = raw_data
        self.clean_data = None

class User_data_cleaning(DataCleaning):
    '''
    Child class for cleaning raw user data
    '''
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def clean_user_data(self):
        '''
        clean users data table
        :return: dataframe
        '''
        user_data = self.raw_data[self.raw_data.email_address.str.contains('@') == True]
        user_data['country_code'] = user_data['country_code'].str.replace('GGB', 'GB')
        user_data['date_of_birth'] = pd.to_datetime(user_data['date_of_birth'], format='mixed')  #
        user_data['join_date'] = pd.to_datetime(user_data['join_date'], format='mixed')          # these lines should only be 1 line
        user_data['Dates_check'] = user_data['join_date'] - user_data['date_of_birth']
        user_data = user_data[(user_data['Dates_check'] > pd.Timedelta(0))]     #
        user_data = user_data.drop('Dates_check', axis=1)                       #
        self.clean_data = user_data

class Card_data_cleaning(DataCleaning):
    '''
    Child class for cleaning card details data
    '''
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.card_details = None
        self.card_spec = None


    def __get_card_type_specs(self):
        '''
        Private method for importing card number specifications for different card types
        '''
        import json
        with open('keys/card_verification.JSON','r') as file:
            self.card_spec = json.load(file)


    def __card_check(self, row):
        '''
        Private method for validating the card numbers follow the consistent format for the relative card type
        :param row: takes a row from the card data dataframe
        '''
        self.__get_card_type_specs()
        card_type = row[2]
        card_number = row[0]
        card_criteria = self.card_spec[card_type]  
        length_check = (card_criteria['minimum card length'] <= len(card_number) <= card_criteria['maximum card length'])
        sequence_lengths = card_criteria['position']
        id_sequence = set([card_number[0:x] for x in sequence_lengths])
        sequence_matches = id_sequence & set(card_criteria['sequence'])
        sequence_verification = len(sequence_matches) >= 1
        return length_check == True and sequence_verification == True

    
    def clean_card_details(self):
        '''
        Method for cleaning card data table
        :return: dataframe
        '''
        card_data = self.raw_data[(self.raw_data.expiry_date.str.len() == 5)]
        card_data = card_data.astype({'card_number':'str'})
        card_data = card_data[card_data.card_number.str.isnumeric() == True]
        card_data['card_details_verified'] = card_data.apply(self.__card_check, axis=1)
        card_data = card_data[card_data.card_details_verified == True]
        card_data['date_payment_confirmed'] = pd.to_datetime(card_data['date_payment_confirmed'], format='mixed')
        card_data['new_expiry_date'] = '20' + card_data.expiry_date.str[3:] + '-' + card_data.expiry_date.str[0:2] + '-01'
        card_data['new_expiry_date'] = pd.to_datetime(card_data['new_expiry_date'], format='%Y-%m-%d')
        card_data['date_payment_confirmed'] = pd.to_datetime(card_data['date_payment_confirmed'], format='%Y-%m-%d')
        card_data['card_valid_at_payment'] = card_data['new_expiry_date'] - card_data['date_payment_confirmed']
        card_data = card_data[(card_data['card_valid_at_payment'] > pd.Timedelta(0))]
        card_data = card_data.drop('new_expiry_date', axis=1)       #
        card_data = card_data.drop('card_valid_at_payment', axis=1) #implement into single line.
        self.clean_data = card_data

class Store_data_cleaning(DataCleaning):
    '''
    Child class for cleaning store data
    '''
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def clean_store_data(self):
        '''
        Method for cleaning store data table
        :return: dataframe
        '''
        store_data = self.raw_data
        store_data = store_data.drop_duplicates()
        store_data = store_data.drop(columns='lat')
        store_data = store_data[store_data.country_code.str.len() == 2]
        store_data['continent'] = store_data['continent'].str.replace('ee', '')
        store_data['address'] = store_data['address'].str.replace('\n', ', ')
        store_data['staff_numbers'] = store_data['staff_numbers'].apply(lambda x: ''.join([i for i in x if i.isnumeric()]))
        store_data[(store_data.apply(lambda row: row['locality'] in row['address'], axis=1))]
        store_data = store_data.set_index('index')
        store_data['opening_date'] = pd.to_datetime(store_data['opening_date'], format='mixed')
        self.clean_data = store_data
        
class Product_data_cleaning(DataCleaning):
    '''
    Child class for cleaning product data
    '''
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def __unit_converter(self, row):
        '''
        Private method for identifying unit type and converting the measurment into kilograms
        :param row: takes a row from the products data dataframe
        '''
        if row[2][-2:] == 'kg':
            return row[2][:-2]
        elif row[2][-2:] == 'ml':
            return int(row[2][:-2])/1000
        elif row[2][-2:] == 'oz':
            return int(row[2][:-2])*0.0284131
        elif row[2][-1:] == 'g':
            try:
                float(row[2][:-1])
                return float(row[2][:-1])/1000
            except ValueError:
                cal = row[2][:-1].split()
            return str(int(cal[0]) * int(cal[2]) / 1000)
        else:
            return 'fail'

    def clean_products_data(self):
        '''
        Method for cleaning products data table
        :return: dataframe
        '''
        products_data = pd.read_csv(self.raw_data)
        products_data.set_index('Unnamed: 0', inplace=True)
        products_data.loc[1779] = products_data.loc[1779].str.replace('77g .','77g')
        products_data['removed'] = products_data['removed'].str.replace('Still_avaliable', 'Still_available')
        products_data = products_data[products_data.uuid.str.len() == 36]
        products_data['date_added'] = pd.to_datetime(products_data['date_added'], format='mixed')
        products_data['product_price'] = products_data.apply(lambda x: (x[1][1:]), axis=1)
        products_data['weight'] = products_data.apply(self.__unit_converter, axis=1)
        products_data['product_price'] = products_data['product_price'].astype('float')
        products_data['weight'] = products_data['weight'].astype('float')
        self.clean_data = products_data

class Order_data_cleaning(DataCleaning):
    '''
    Child class for cleaning order data
    '''
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def clean_orders_data(self):
        '''
        Method for cleaning orders data table
        :return: dataframe
        '''
        orders_data = self.raw_data.drop(['first_name', 'last_name', '1'], axis=1)
        orders_data.set_index('index', inplace=True)
        orders_data.drop('level_0', axis=1, inplace=True)
        self.clean_data = orders_data

class Date_data_cleaning(DataCleaning):
    '''
    Child class for cleaning raw date data
    '''
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def clean_date_details(self):
        '''
        Method for cleaning date data table
        :return: dataframe
        '''
        date_data = pd.read_json(self.raw_data)
        date_data = date_data[date_data.month.str.isnumeric() == True]
        date_data['month'] = date_data['month'].apply(lambda x: f"{int(x):02}")
        date_data['day'] = date_data['day'].apply(lambda x: f"{int(x):02}")
        self.clean_data = date_data