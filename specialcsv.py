import sqlite3
import numpy as np #type: ignore
import pandas as pd # type: ignore

# from db_scripts import *
from dbconnection import connectToDB
from db import DB
# from enviornment_variables import csv_file

csv_file = '../spreadsheets/csv/PresidentialElectionHistoryFINAL.csv'

# Setting up sqlite database
con = sqlite3.connect('db.sqlite3')

# Creating the sqlite database
working_db = DB(con)
working_db.createDB()
cur = con.cursor()

def strToIntComplex(strnum: str) -> int:
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

# Migrate this into the class
def handleData(raw_data: list) -> None:
    office_data = [
        working_db.createOrGetOfficePosition('President'),
        working_db.createOrGetOfficePosition('Vice President')
    ]
    # This is the initial data that we need to properly save the data to the db
    data = {
        'election_year': raw_data[0],
        'party': raw_data[1],
        'president_name': raw_data[2],
        'vice_president_name': raw_data[3],
        'popular_vote': strToIntComplex(raw_data[4]),
        'total_population': strToIntComplex(raw_data[5]),
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

# con.commit()
# con.close()
working_db.deactivate()


class SpecialCSV:
    # This is created specifically to upload the president and vice president data
    def __init__(self, db_name: str, csv: str, header: int = 0):
        self.db_name = db_name
        self.csv = csv
        self.header = header

    def upload(self) -> None:
        try:
            raw_data = pd.read_csv(filepath_or_buffer=self.csv, header=self.header)
            for row in raw_data:
                print(f'Processing: {row}')
            print('Saved new data.')
        except Exception as e:
            print('Not able to mine the data:',e)

    def handleData(self, raw_data: list) -> None:
        pass
