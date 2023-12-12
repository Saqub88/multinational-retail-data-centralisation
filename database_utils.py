import yaml
import sqlalchemy

class DatabaseConnector:
    def __init__(self):
        self.database_credentials = None
        self.engine = None
        self.list_tables = None
     
    def read_db_creds(self, credential_file):
        with open(credential_file, 'r') as file:
            self.database_credentials = yaml.safe_load(file)

    def init_db_engine(self):
        self.engine = sqlalchemy.create_engine(
            f"postgresql+psycopg2://{self.database_credentials['RDS_USER']}"
            f":{self.database_credentials['RDS_PASSWORD']}"
            f"@{self.database_credentials['RDS_HOST']}"
            f":{self.database_credentials['RDS_PORT']}"
            f"/{self.database_credentials['RDS_DATABASE']}"
        )

    def list_db_tables(self):
        inspector = sqlalchemy.inspect(self.engine)
        self.list_tables = inspector.get_table_names()

    def upload_to_db(self, pd_df, table_name):
        localengine = sqlalchemy.create_engine('postgresql://postgres:5150@localhost:5432/Sales_data')
        pd_df.to_sql(table_name, localengine, if_exists='replace')
    
    def upload_to_sqlite(self, df, table_name):
        localengine = sqlalchemy.create_engine("sqlite:///sales_data.db")
        df.to_sql(table_name, localengine, if_exists='replace')