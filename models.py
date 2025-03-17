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


class CandidatesToElections:
    table_script = """
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

    def __init__(self, db_name: str, id: int=-1, popular_vote: int=0, electoral_vote: int=0, notes: str='', won: bool=False, election_id: int=-1, candidate_id: int=-1):
        self.db_name = db_name
        self.id = id
        self.popular_vote = popular_vote
        self.electoral_vote = electoral_vote
        self.notes = notes
        self.won = won
        self.election_id = election_id
        self.candidate_id = candidate_id

    @classmethod
    def createCandidateToElection(cls, data: dict):
        # query = "INSERT OR IGNORE INTO candidates_to_elections (popular_vote, electoral_vote, notes, won, election_id, candidate_id) VALUES ( ?, ?, ?, ?, ?, ? )"
        query = "INSERT OR IGNORE INTO candidates_to_elections (popular_vote, electoral_vote, notes, won, election_id, candidate_id) VALUES ( %(popular_vote)s, %(electoral_vote)s, %(notes)s, %(won)s, %(election_id)s, %(candidate_id)s )"
        return connectToDB(cls.db_name).query_db(query, data)

    @classmethod
    def getCandidateElectionByCandidate(cls, data: dict): 
        # Fix this later
        return None


class CandidatesToParty:
    table_script = """
    CREATE TABLE IF NOT EXISTS candidates_to_party (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id REFERENCES candidates (id) ON DELETE CASCADE,
        party_id REFERENCES political_party (id) ON DELETE CASCADE
    );
    """

    def __init__(self, db_name: str, id: int=-1, candidate_id: int=-1, party_id: int=-1):
        self.db_name = db_name
        self.id = id
        self.candidate_id = candidate_id
        self.party_id = party_id

    @classmethod
    def createCandidateToParty(cls, data: dict):
        # query = "INSERT OR IGNORE INTO candidates_to_party (candidate_id, party_id) VALUES ( ?, ? )"
        query = "INSERT OR IGNORE INTO candidates_to_party (candidate_id, party_id) VALUES ( %(candidate_id)s, %(party_id)s )"
        return connectToDB(cls.db_name).query_db(query, data)

    @classmethod
    def getCandidatePartyByCandidate(cls, data: dict):
        # Fix this later
        return None


class CandidatesToOffice:
    table_script = """
    CREATE TABLE IF NOT EXISTS candidates_to_office (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id REFERENCES candidates (id) ON DELETE CASCADE,
        office_id REFERENCES office_position (id) ON DELETE CASCADE
    );
    """

    def __init__(self, db_name: str, id: int=-1, candidate_id: int=-1, office_id: int=-1):
        self.db_name = db_name
        self.id = id
        self.candidate_id = candidate_id
        self.office_id = office_id

    @classmethod
    def createCandidateToOffice(cls, data: dict):
        # query = "INSERT OR IGNORE INTO candidates_to_office (candidate_id, office_id) VALUES ( ?, ? )"
        query = "INSERT OR IGNORE INTO candidates_to_office (candidate_id, office_id) VALUES ( %(candidate_id)s, %(office_id)s )"
        return connectToDB(cls.db_name).query_db(query, data)

    @classmethod
    def getCandidateOfficeByCandidate(cls, data: dict):
        # Fix this later
        return None