# SQL scripts needed to get things to work
election_year_script = """
CREATE TABLE IF NOT EXISTS election_year (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER UNIQUE,
    total_population INTEGER NOT NULL,
    total_electoral INTEGER NOT NULL
);
"""

political_party_script = """
CREATE TABLE IF NOT EXISTS political_party (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    party TEXT UNIQUE
);
"""

office_position_script = """
CREATE TABLE IF NOT EXISTS office_position (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position TEXT UNIQUE
);
"""

candidates_script = """
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);
"""

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