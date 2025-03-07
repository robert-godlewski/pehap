import sqlite3

from db_scripts import *


class DB:
    # Used to interact with a SQLite db
    def __init__(self, con: sqlite3.Connection):
        self.con = con
        self.cur = con.cursor()
        self.tables_scripts = [
            {'table_name': 'election_year', 'script': election_year_script},
            {'table_name': 'political_party', 'script': political_party_script},
            {'table_name': 'office_position', 'script': office_position_script},
            {'table_name': 'candidates', 'script': candidates_script},
            {'table_name': 'candidates_to_elections', 'script': candidates_to_elections_script},
            {'table_name': 'candidates_to_party', 'script': candidates_to_party_script},
        ]

    def createDB(self):
        table = 0
        db_ok = True
        while db_ok and table < len(self.tables_scripts):
            db_ok = self._createTable(table)
            table += 1
        if not db_ok:
            print('Something is wrong with making one of the tables!')
        self.con.commit()

    def deactivate(self):
        # Saves and closes the db session
        self.con.commit()
        self.con.close()

    def _createTable(self, table: int) -> bool:
        # Creates tables in the db
        try:
            self.cur.execute(self.tables_scripts[table]['script'])
            print(f'Loading/ Creating {self.tables_scripts[table]['table_name']}.')
            return True
        except sqlite3.OperationalError:
            print(f'Failed to create and load {self.tables_scripts[table]['table_name']}.')
            return False

    def createOrGetOfficePosition(self, position: str) -> dict:
        self.cur.execute("INSERT OR IGNORE INTO office_position (position) VALUE ( ? )", (position,))
        self.cur.execute("SELECT * FROM office_position WHERE position = ? ", (position,))
        raw = self.cur.fetchone()
        return {
            'id': raw[0],
            'position': raw[1]
        }

    def createOrGetElectionYear(self, in_data: dict) -> dict:
        self.cur.execute("INSERT OR IGNORE INTO election_year (year, total_population, total_electoral) VALUES ( ?, ?, ? )", (in_data['year'], in_data['total_population'],in_data['total_electoral'],))
        self.cur.execute("SELECT * FROM election_year WHERE year = ? ", (in_data['year'],))
        data = self.cur.fetchone()
        return {
            'id': data[0],
            'total_population': data[1],
            'total_electoral': data[2]
        }

    def createOrGetParty(self, in_data: dict) -> dict:
        self.cur.execute("INSERT OR IGNORE INTO political_party (party) VALUES ( ? )", (in_data['party'],))
        self.cur.execute("SELECT * FROM political_party WHERE party = ? ", (in_data['party'],))
        data = self.cur.fetchone()
        return {
            'id': data[0],
            'party': data[1]
        }

    def createOrGetCandidate(self, in_data: dict, key: str) -> dict:
        self.cur.execute("INSERT OR IGNORE INTO cadidates (name) VALUES ( ? )", (in_data[key],))
        self.cur.execute("SELECT * FROM cadidates WHERE name = ? ", (in_data[key],))
        data = self.cur.fetchone()
        return {
            'id': data[0],
            'name': data[1]
        }

    def createCandidateElection(self, base_data: dict, year_data: dict, candidate_data: dict) -> None:
        self.cur.execute("INSERT OR IGNORE INTO candidates_to_elections (popular_vote, electoral_vote, notes, won, election_id, candidate_id) VALUES ( ?, ?, ?, ?, ?, ? )", (base_data['popular_vote'], base_data['electoral_vote'], base_data['notes'], base_data['won'], year_data['id'], candidate_data['id'],))

    def createCandidateParty(self, candidate_id: int, party_id: int) -> None:
        self.cur.execute("INSERT OR IGNORE INTO candidates_to_party (candidate_id, party_id) VALUES ( ?, ? )", (candidate_id, party_id,))

    def createCandidateOffice(self, candidate_id: int, office_id: int) -> None:
        self.cur.execute("INSERT OR IGNORE INTO candidates_to_office (candidate_id, office_id) VALUES ( ?, ? )", (candidate_id, office_id,))