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

def _createOrGetOfficePosition(position: str) -> dict:
    cur.execute("INSERT OR IGNORE INTO office_position (position) VALUE ( ? )", (position,))
    cur.execute("SELECT * FROM office_position WHERE position = ? ", (position,))
    raw = cur.fetchone()
    return {
        'id': raw[0],
        'position': raw[1]
    }

def getOfficeData() -> list:
    president = _createOrGetOfficePosition('President')
    vice_president = _createOrGetOfficePosition('Vice President')
    return [president, vice_president]

def createOrGetElectionYear(year: int, total_population: int, total_electoral: int) -> dict:
    cur.execute("INSERT OR IGNORE INTO election_year (year, total_population, total_electoral) VALUES ( ?, ?, ? )", (year, total_population,total_electoral,))
    cur.execute("SELECT * FROM election_year WHERE year = ? ", (year,))
    data = cur.fetchone()
    return {
        'id': data[0],
        'total_population': data[1],
        'total_electoral': data[2]
    }

def createOrGetParty(party: str) -> dict:
    cur.execute("INSERT OR IGNORE INTO political_party (party) VALUES ( ? )", (party,))
    cur.execute("SELECT * FROM political_party WHERE party = ? ", (party,))
    data = cur.fetchone()
    return {
        'id': data[0],
        'party': data[1]
    }

def createOrGetCandidate(candidate: str) -> dict:
    cur.execute("INSERT OR IGNORE INTO cadidates (name) VALUES ( ? )", (candidate,))
    cur.execute("SELECT * FROM cadidates WHERE name = ? ", (candidate,))
    data = cur.fetchone()
    return {
        'id': data[0],
        'name': data[1]
    }

def createCandidateElection(popular_vote: int, electoral_vote: int, notes: str, won: bool, election_id: int, candidate_id: int) -> None:
    cur.execute("INSERT OR IGNORE INTO candidates_to_elections (popular_vote, electoral_vote, notes, won, election_id, candidate_id) VALUES ( ?, ?, ?, ?, ?, ? )", (popular_vote, electoral_vote, notes, won, election_id, candidate_id,))

def createCandidateParty(candidate_id: int, party_id: int) -> None:
    cur.execute("INSERT OR IGNORE INTO candidates_to_party (candidate_id, party_id) VALUES ( ?, ? )", (candidate_id, party_id,))

def createCandidateOffice(candidate_id: int, office_id: int) -> None:
    cur.execute("INSERT OR IGNORE INTO candidates_to_office (candidate_id, office_id) VALUES ( ?, ? )", (candidate_id, office_id,))

def handleData(data: list) -> None:
    office_data = getOfficeData()
    # We can just calculate data[6] and data[9] later
    election_year = data[0]
    party = data[1]
    president_name = data[2]
    vice_president_name = data[3]
    popular_vote = _strToInt(data[4])
    total_population = _strToInt(data[5])
    electoral_vote = data[7]
    total_electoral = data[8]
    notes = data[10]
    won = data[11]
    year_data = createOrGetElectionYear(election_year, total_population, total_electoral)
    party_data = createOrGetParty(party)
    president_data = createOrGetCandidate(president_name)
    createCandidateElection(popular_vote, electoral_vote, notes, won, election_id=year_data['id'], candidate_id=president_data['id'])
    createCandidateParty(candidate_id=president_data['id'], party_id=party_data['id'])
    createCandidateOffice(candidate_id=president_data['id'], office_id=office_data[0]['id'])
    vice_president_data = createOrGetCandidate(vice_president_name)
    createCandidateElection(popular_vote, electoral_vote, notes, won, election_id=year_data['id'], candidate_id=vice_president_data['id'])
    createCandidateParty(candidate_id=vice_president_data['id'], party_id=party_data['id'])
    createCandidateOffice(candidate_id=vice_president_data['id'], office_id=office_data[1]['id'])


try:
    # We will not need the first couple of lines within the csv file
    header = 1
    raw_data = pandas.read_csv(csv_file,header=header).values
    print(raw_data.shape)
    print(raw_data[0])
    # print(raw_data[1])
    print(f'{raw_data[0][4]}: {type(raw_data[0][4])}')
    num = _strToInt(raw_data[0][4])
    print(f'{num}: {type(num)}')
    # numpy.save(npy_temp_name,data)
    for row in raw_data:
        handleData(row)
    print('Saved new data.')
except:
    print('There is no data to mine with the necessary information!')

con.commit()
con.close()