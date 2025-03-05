import sqlite3
import numpy #type: ignore
import pandas # type: ignore

# from db_scripts import *
from db import DB
from enviornment_variables import csv_file

# Setting up sqlite database
con = sqlite3.connect('db.sqlite3')

# Creating the sqlite database
working_db = DB(con)
working_db.createDB()
cur = con.cursor()

def strToInt(strnum: str) -> int:
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

def getOfficeData() -> list:
    president = working_db.createOrGetOfficePosition('President')
    vice_president = working_db.createOrGetOfficePosition('Vice President')
    return [president, vice_president]

def handleData(raw_data: list) -> None:
    office_data = getOfficeData()
    # This is the initial data that we need to properly save the data to the db
    # We can just calculate raw_data[6] and raw_data[9] later
    data = {
        'election_year': raw_data[0],
        'party': raw_data[1],
        'president_name': raw_data[2],
        'vice_president_name': raw_data[3],
        'popular_vote': strToInt(raw_data[4]),
        'total_population': strToInt(raw_data[5]),
        # We don't need to save raw_data[6] because we can just calculate this later
        'electoral_vote': raw_data[7],
        'total_electoral_vote': raw_data[8],
        # We don't need to save raw_data[9] because we can just calculate this later
        'notes': raw_data[10],
        'won': raw_data[11],
    }
    year_data = working_db.createOrGetElectionYear(data)
    party_data = working_db.createOrGetParty(data)
    president_data = working_db.createOrGetCandidate(data,'president_name')
    working_db.createCandidateElection(data, year_data, president_data)
    working_db.createCandidateParty(candidate_id=president_data['id'], party_id=party_data['id'])
    working_db.createCandidateOffice(candidate_id=president_data['id'], office_id=office_data[0]['id'])
    vice_president_data = working_db.createOrGetCandidate(data,'vice_president_name')
    working_db.createCandidateElection(data, year_data, vice_president_data)
    working_db.createCandidateParty(candidate_id=vice_president_data['id'], party_id=party_data['id'])
    working_db.createCandidateOffice(candidate_id=vice_president_data['id'], office_id=office_data[1]['id'])


try:
    # We will not need the first couple of lines within the csv file
    header = 1
    raw_data = pandas.read_csv(csv_file,header=header).values
    # print(raw_data.shape)
    # print(raw_data[0])
    # print(raw_data[1])
    # print(f'{raw_data[0][4]}: {type(raw_data[0][4])}')
    # num = strToInt(raw_data[0][4])
    # print(f'{num}: {type(num)}')
    # numpy.save(npy_temp_name,data)
    for row in raw_data:
        handleData(row)
    print('Saved new data.')
except:
    print('There is no data to mine with the necessary information!')

# con.commit()
# con.close()
working_db.deactivate()
