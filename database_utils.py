import yaml
import sqlalchemy


class DatabaseConnector:
        # class creator. no need to take in any parameters. maybe create a single parameter to take in credentials file ?
    def __init__(self):
        self.database_credentials = None
        self.engine = None
        self.list_tables = None
    
        # converts credentials file into dictionary which in turn will be used to create sql_engine 
    def read_db_creds(self, credential_file):
        with open(credential_file, 'r') as file:
            self.database_credentials = yaml.safe_load(file)

        # need to find a way which allows me to split the line down. too long. poor readability. tried f''' but doesn't like line being split.
        # keys all start with RDS_ ... wont work with any other credentials file if formatting is changed.
        # postgresql uses psycopg2 as default so can cut '+psycopg2' from string. For SQlite engine = create_engine("sqlite:///foo.db") uses sqlite3 by default. 
    def init_db_engine(self):
        self.engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{self.database_credentials['RDS_USER']}:{self.database_credentials['RDS_PASSWORD']}@{self.database_credentials['RDS_HOST']}:{self.database_credentials['RDS_PORT']}/{self.database_credentials['RDS_DATABASE']}")

        # retrieves the list of tables.
    def list_db_tables(self):
        inspector = sqlalchemy.inspect(self.engine)
        self.list_tables = inspector.get_table_names()

    # perhaps create a single method which takes in the credential files and then run all methods.
    # perhaps going further and allow an extra method or an option within current method to use SQLite
    def upload_to_db(self, pd_df, table_name):
        localengine = sqlalchemy.create_engine('postgresql://postgres:5150@localhost:5432/Sales_data')
        pd_df.to_sql(table_name, localengine, if_exists='replace')
    
    def upload_to_sqlite(self, df, table_name):
        localengine = sqlalchemy.create_engine("sqlite:///sales_data.db")
        df.to_sql(table_name, localengine, if_exists='replace')