# Multinational retail data cetralisation.

This has been an eventful adventure of mixing both old and new skills. Previously learnt skill included the use of python and OOP while also implementing newly learnt skills with pandas, some sql, use of boto3, sqlalchemy etc, data cleaning etc. 
First steps are often the hardest but as the tasks went on, things began to get easier as some aspects repeated themselves.

## Milestone 2

Using a skeleton of the 3 classes (data_cleaning.py, data_extraction.py and database_utils.py), the task was to develop code which would implement methods that extract raw data, clean the data and upload the dataframes to a database. i added a few extra challenges such as creating additional methods for uploading the dataframes to different databases, private methods which are used with the cleaning of some of the data, functions which run all the methods for any particular database and a code which manages all these functions and classes.

To extract any table to a required database I have developed a python file M2_simple_extractor.py. As i had found myself repeatedly ammending and reuploading tables manually i found it easier to develop a file which did all the work for me. i just had to input which tables i wanted and where i want them uploaded to and the code would organise it for me. It works in conjunction with the extractor_functions.py file (also by my creation) to run the sequences required to extract, clean and upload a table to the required database. 

There is a part of the M2_simple_extractor.py which takes the input from the user and then cleans the string into a list of only valid characters without duplicates. The code was still in development and i assumed i would have the could iterate through this list instead of searching the list but seems it doesnt actually serve much of a purpose other than to convert the string to list. i have left it in there on the offchance that if i work on the code at a further point in time, it may be useful if i restructure the way the file works.

## Milestone 3

this exercise was effectively completed twice over as the codes to reformat the tables would differ for postgresql and sqlite. It was a helpful exercise as it demonstrated the differences between the two.
The SQL files themselves are located within the 'sql_files' folder. then depending on which database you are working with (either SQlite or Postgresql) then the respective sql files may be found within these folders.
For ease i have created also a single SQL file which is composed of all the other SQL files to complete the tast in a single file and then the table specific files may be accessed if there is a need to run the sequence for a single table only (for troubleshooting or incase a table is deleted in error.)

I did make an attempt to have each of the files run through python utilising SQLalchemy but unfortunately i was only able to get it partially working. i may revisit this at a later stage to get it working. (the current model is the file M3_sql_table_formatting.py)
I have only used SQLite so far but i found that SQL is unable to change datatypes without having to recreate the table. SQL alchemy appears to have no trouble renaming the original table to a backup and creating a new table with the required column names and assigning the data type but the transfer of data from the backup to the new table doesnt work via this method. it returns no errors but the tables are still empty after.

For PGadmin just need to run each sql file against database but may need to run the primary key settings prior to the foreign keys.

## Milestone 4.

The sql files are found in the 'sql_files/Milestone 4' folder. The final task gave the most difficulty as I was unable to get the exact figures as shown on the portal webpage. Upon speaking to one of the engineers, it appears that the dispcrepancies may be related to how the data may have been cleaned. These should work for both SQLite and PostgreSQL with the exception of the final task. 