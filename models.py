# Contains a group of models to help convert data
from dbconnection import connectToDB


class ElectionYear:
    table_script = """
    CREATE TABLE IF NOT EXISTS election_year (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER UNIQUE,
        total_population INTEGER NOT NULL,
        total_electoral INTEGER NOT NULL
    );
    """

    def __init__(self, db_name: str, id: int=-1, year: int=-1, total_population: int=-1, total_electoral: int=-1) -> None:
        self.db_name = db_name
        self.id = id
        self.year = year
        self.total_population = total_population
        self.total_electoral = total_electoral

    @classmethod
    def createEY(cls, data: dict):
        # query = "INSERT OR IGNORE INTO election_year (year, total_population, total_electoral) VALUES ( ?, ?, ? )"
        query = "INSERT OR IGNORE INTO election_year (year, total_population, total_electoral) VALUES ( %(year)s, %(total_population)s, %(total_electoral)s )"
        return connectToDB(cls.db_name).query_db(query, data)

    @classmethod
    def getEYbyYear(cls, data: dict):
        # query = "SELECT * FROM election_year WHERE year = ? "
        query = "SELECT * FROM election_year WHERE year = %(year)s;"
        results = connectToDB(cls.db_name).query_db(query, data)
        return cls(results[0])


class PoliticalParty:
    table_script = """
    CREATE TABLE IF NOT EXISTS political_party (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        party TEXT UNIQUE
    );
    """

    def __init__(self, db_name: str, id: int=-1, party: str='') -> None:
        self.db_name = db_name
        self.id = id
        self.party = party

    @classmethod
    def createParty(cls, data: dict):
        # query = "INSERT OR IGNORE INTO political_party (party) VALUES ( ? )"
        query = "INSERT OR IGNORE INTO political_party (party) VALUES ( %(party)s )"
        return connectToDB(cls.db_name).query_db(query, data)

    @classmethod
    def getPartyByName(cls, data: dict):
        # query = "SELECT * FROM political_party WHERE party = ? "
        query = "SELECT * FROM political_party WHERE party = %(party)s;"
        results = connectToDB(cls.db_name).query_db(query, data)
        return cls(results[0])


class OfficePosition:
    table_script = """
    CREATE TABLE IF NOT EXISTS office_position (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position TEXT UNIQUE
    );
    """

    def __init__(self, db_name: str, id: int=-1, position: str='') -> None:
        self.db_name = db_name
        self.id = id
        self.position = position

    @classmethod
    def createOffice(cls, data: dict):
        # query = "INSERT OR IGNORE INTO office_position (position) VALUE ( ? )"
        query = "INSERT OR IGNORE INTO office_position (position) VALUE ( %(position)s )"
        return connectToDB(cls.db_name).query_db(query, data)

    @classmethod
    def getOfficeByPosition(cls, data: dict):
        # query = "SELECT * FROM office_position WHERE position = ? "
        query = "SELECT * FROM office_position WHERE position = %(position)s;"
        results = connectToDB(cls.db_name).query_db(query, data)
        return cls(results[0])


class Candidates:
    table_script = """
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );
    """

    def __init__(self, db_name: str, id: int=-1, name: str ='') -> None:
        self.db_name = db_name
        self.id = id
        self.name = name

    @classmethod
    def createCandidate(cls, data: dict):
        # query = "INSERT OR IGNORE INTO cadidates (name) VALUES ( ? )"
        query = "INSERT OR IGNORE INTO cadidates (name) VALUES ( %(name)s )"
        return connectToDB(cls.db_name).query_db(query, data)

    @classmethod
    def getCandidateByName(cls, data: dict):
        # query = "SELECT * FROM cadidates WHERE name = ? "
        query = "SELECT * FROM cadidates WHERE name = %(name)s;"
        results = connectToDB(cls.db_name).query_db(query, data)
        return cls(results[0])

# FIX BELOW
# All were from db_scripts.py
candidates_to_elections_script = """
CREATE TABLE IF NOT EXISTS candidates_to_elections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    popular_vote INTEGER NOT NULL,
    electoral_vote INTEGER NOT NULL,
    notes TEXT,
    won TEXT DEFAULT FALSE,
    election_id REFERENCES election_year (id) ON DELETE CASCADE,
    candidate_id REFERENCES candidates (id) ON DELETE CASCADE
);
"""

candidates_to_party_script = """
CREATE TABLE IF NOT EXISTS candidates_to_party (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id REFERENCES candidates (id) ON DELETE CASCADE,
    party_id REFERENCES political_party (id) ON DELETE CASCADE
);
"""

candidates_to_office_script = """
CREATE TABLE IF NOT EXISTS candidates_to_office (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id REFERENCES candidates (id) ON DELETE CASCADE,
    office_id REFERENCES office_position (id) ON DELETE CASCADE
);
"""