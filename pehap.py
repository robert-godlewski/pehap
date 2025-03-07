from dbconnection import connectToDB
from db_scripts import election_year_script, political_party_script, office_position_script, candidates_script, candidates_to_elections_script, candidates_to_party_script, candidates_to_office_script


def createDBtables(db_name: str) -> None:
    tables_scripts = [
        {'table_name': 'election_year', 'script': election_year_script},
        {'table_name': 'political_party', 'script': political_party_script},
        {'table_name': 'office_position', 'script': office_position_script},
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


if __name__ == '__main__':
    print('This is the main program')
    db_name = 'db.sqlite3'
    createDBtables(db_name)
    # csv_file = 'spreadsheets/csv/PresidentialElectionHistoryFINAL.csv'
    # header = 1 # This is for the elections
    # Add in uploading csv scripts
    # Add in graphing scripts
