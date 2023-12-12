import sqlalchemy
from sqlalchemy import text
import os

file_list = os.listdir('sql_files/modify column datatypes/sqlite')

full_sequence = ''
for file in file_list:
    with open(f"sql_files/modify column datatypes/sqlite/{file}") as part_sequence:
        full_sequence = full_sequence + part_sequence.read()
final = full_sequence.split(';')
final.remove('')
print(final)

engine = sqlalchemy.create_engine("sqlite:///test_db.db")

for x in final:
    with engine.connect() as connection:
        connection.execute(text(x))