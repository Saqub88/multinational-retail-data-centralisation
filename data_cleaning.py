
import pandas as pd

class DataCleaning():
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.clean_data = None

    def clean_user_data(self):
        user_data = self.raw_data[self.raw_data.email_address.str.contains('@') == True]
        user_data['country_code'] = user_data['country_code'].str.replace('GGB', 'GB')
        user_data['date_of_birth'] = pd.to_datetime(user_data['date_of_birth'], format='mixed')
        user_data['join_date'] = pd.to_datetime(user_data['join_date'], format='mixed')
        user_data['Dates_check'] = user_data['join_date'] - user_data['date_of_birth']
        user_data = user_data[(user_data['Dates_check'] > pd.Timedelta(0))]
        user_data = user_data.drop('Dates_check', axis=1)
        self.clean_data = user_data

    def __card_check(self, row):
        if row[2] == 'JCB 16 digit':
            if len(row[0]) == 16 and row[0][0:2] == '35':
                return True
        elif row[2] == 'JCB 15 digit':
            if len(row[0]) == 15 and (row[0][0:4] == '1800' or '2131'):
                return True
        elif row[2] == 'VISA 19 digit':
            if len(row[0]) == 19 and row[0][0:1] == '4':
                return True
        elif row[2] == 'VISA 16 digit':
            if len(row[0]) == 16 and row[0][0:1] == '4':
                return True
        elif row[2] == 'VISA 13 digit':
            if len(row[0]) == 13 and row[0][0:1] == '4':
                return True
        elif row[2] == 'Diners Club / Carte Blanche':
            if len(row[0]) == 14 and ((row[0][0:3] == '300' or '301' or '302' or '303' or '304' or '305') or (row[0][0:2] == '36' or '38' or '39')):
                return True
        elif row[2] == 'American Express':
            if len(row[0]) == 15 and row[0][0:2] == '34' or '37':
                return True
        elif row[2] == 'Maestro':
            if (len(row[0]) >= 16 and len(row[0]) <= 19) and ((row[0][0:2] == '50' or '56' or '57' or '58') or (row[0][0:4] == '6013')):
                return True
        elif row[2] == 'Mastercard':
            if len(row[0]) == 16 and ((50 <= int(row[0][0:2]) <= 55) or ((2221 <= int(row[0][0:4]) <= 2720))):
                return True
        elif row[2] == 'Discover':
            if len(row[0]) == 16 and ((row[0][0:2] == '65') or (row[0][0:3] == '644' or '645' or '646' or '647' or '648' or '649') or (row[0][0:4] == '6011')):
                return True
        else:
            return False

    
    def clean_card_details(self):
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
        card_data = card_data.drop('new_expiry_date', axis=1)
        card_data = card_data.drop('card_valid_at_payment', axis=1) #implement line 70, 71 into single line.
        self.clean_data = card_data
    # consider looking at resetting the index on the data once cleaned (be careful to ensure that index isn't a shared piece of data between other tables)

    def clean_store_data(self):
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
        
    
    def __unit_converter(self, row):
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
        df = pd.read_csv(self.raw_data)
        df = df.rename(columns={'weight': 'weight (kg)', 'Unnamed: 0':'index', 'product_price':'product_price (£)'})
        df = df.set_index('index')
        df.loc[1779] = df.loc[1779].str.replace('77g .','77g')
        df['removed'] = df['removed'].str.replace('Still_avaliable', 'Still_available')
        df = df[df.uuid.str.len() == 36]
        df['date_added'] = pd.to_datetime(df['date_added'], format='mixed')
        df['product_price (£)'] = df.apply(lambda x: (x[1][1:]), axis=1)
        df['weight (kg)'] = df.apply(self.__unit_converter, axis=1)
        df['product_price (£)'] = df['product_price (£)'].astype('float')
        df['weight (kg)'] = df['weight (kg)'].astype('float')
        #df = df[df.EAN.str.len() == 13]
        self.clean_data = df
    
    def clean_orders_data(self):
        df = self.raw_data.drop(['first_name', 'last_name', '1'], axis=1)
        df.set_index('index', inplace=True)
        df.drop('level_0', axis=1, inplace=True)
        self.clean_data = df

    def clean_date_details(self):
        df = pd.read_json(self.raw_data)
        df = df[df.month.str.isnumeric() == True]
        df['month'] = df['month'].apply(lambda x: f"{int(x):02}")
        df['day'] = df['day'].apply(lambda x: f"{int(x):02}")
        self.clean_data = df

