import pandas as pd # type: ignore

from dbconnection import connectToDB
from functions import handleData
from models import ElectionYear, PoliticalParty, OfficePosition, candidates_script, candidates_to_elections_script, candidates_to_party_script, candidates_to_office_script # Fix this to only have Classes


def createDBtables(db_name: str) -> None:
    tables_scripts = [
        {'table_name': 'election_year', 'script': ElectionYear.table_script},
        {'table_name': 'political_party', 'script': PoliticalParty.table_script},
        {'table_name': 'office_position', 'script': OfficePosition.table_script},
        {'table_name': 'candidates', 'script': candidates_script},
        {'table_name': 'candidates_to_elections', 'script': candidates_to_elections_script},
        {'table_name': 'candidates_to_party', 'script': candidates_to_party_script},
        {'table_name': 'candidates_to_office', 'script': candidates_to_office_script},
    ]
    table_id = 0
    db_ok = True
    while db_ok and table_id < len(tables_scripts):
        print(f"Attempting to loading or create {tables_scripts[table_id]['table_name']}")
        result = connectToDB(db_name).query_db(tables_scripts[table_id]['script'])
        if not result:
            db_ok = False
            print(f"Something when wrong when trying to load or create {tables_scripts[table_id]['table_name']}")
        table_id += 1

def upload_csv(db_name: str, csv: str, header: int) -> None:
    try:
        csv_data = pd.read_csv(filepath_or_buffer=csv, header=header)
        for row in csv_data:
            print('Processing:', row)
            handleData(db_name, row)
        print('Saved new data.')
    except Exception as e:
        print('Not able to mine the data:', e)


if __name__ == '__main__':
    print('This is the main program')
    db_name = 'db.sqlite3'
    createDBtables(db_name)
    csv_file = 'spreadsheets/csv/PresidentialElectionHistoryFINAL.csv'
    header = 1 # This is for the elections
    upload_csv(db_name,csv_file,header)
    # Add in graphing scripts
