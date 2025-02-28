import sqlite3
import numpy #type: ignore
import pandas # type: ignore

from db_scripts import *
from enviornment_variables import csv_file

# Creating and setting up sqlite database
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

# Creating data tables
def _createTable(table_name: str, script: str) -> bool:
    try:
        cur.execute(script)
        print(f'Loading/ Creating {table_name}.')
        return True
    except sqlite3.OperationalError:
        print(f'Failed to create and load {table_name}.')
        return False

db_ok = True
table = 0
tables_scripts = [
    {'table_name': 'election_year', 'script': election_year_script},
    {'table_name': 'political_party', 'script': political_party_script},
    {'table_name': 'office_position', 'script': office_position_script},
    {'table_name': 'candidates', 'script': candidates_script},
    {'table_name': 'candidates_to_elections', 'script': candidates_to_elections_script},
    {'table_name': 'candidates_to_party', 'script': candidates_to_party_script},
]

while db_ok and table < len(tables_scripts):
    db_ok = _createTable(tables_scripts[table]['table_name'],tables_scripts[table]['script'])
    table += 1

if not db_ok:
    print('Something is wrong with making one of the tables!')

def _strToInt(strnum: str) -> int:
    num_arr = strnum.split(",")
    num = 0
    i = len(num_arr)-1
    multi = 1
    while i >= 0:
        temp = int(num_arr[i])
        temp_mult = temp * multi
        num += (temp_mult-temp)
        i -= 1
        multi += 1000
    return num

# Fix this
def _handleData(data):
    # We can just calculate data[6] and data[9] later
    election_year_data = {
        'year': data[0],
        'total_population': _strToInt(data[5]),
        'total_electoral': data[8],
    }
    political_party_data = {
        'party': data[1]
    }
    office_positions_data = [
        {'position': 'President'},
        {'position': 'Vice President'},
    ]
    candidates_data = [
        # President
        {'name': data[2]},
        # Vice President
        {'name': data[3]}
    ]
    candidates_to_elections_data = {
        'popular_vote': _strToInt(data[4]),
        'electoral_vote': data[7],
        'notes': data[10],
        'won': data[11],
    }
    # Add in sql and more data later
    candidates_to_party_data = {}

try:
    # We will not need the first 2 lines within the csv file
    header = 1
    raw_data = pandas.read_csv(csv_file,header=header).values
    print(raw_data.shape)
    print(raw_data[0])
    # print(raw_data[1])
    print(f'{raw_data[0][4]}: {type(raw_data[0][4])}')
    num = _strToInt(raw_data[0][4])
    print(f'{num}: {type(num)}')
    # numpy.save(npy_temp_name,data)
    # Need to use the _handleData function here
    print('Saved new data.')
except:
    print('There is no data to mine with the necessary information!')

con.commit()
con.close()