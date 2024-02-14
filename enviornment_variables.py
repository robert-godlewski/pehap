wiki = 'https://en.wikipedia.org/'
db_name = 'sql.db'

# Scripts
countries_table = '''
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    name TEXT, 
    title TEXT, 
    links TEXT, 
    year_established INTEGER, 
    month_established TEXT, 
    day_established INTEGER, 
    year_disestablished INTEGER, 
    month_disestablished TEXT, 
    day_disestablished INTEGER
);
'''

admin_divisions_table = '''
CREATE TABLE IF NOT EXISTS admin_divisions (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    name TEXT, 
    title TEXT, 
    links TEXT, 
    year_established INTEGER, 
    month_established TEXT, 
    day_established INTEGER, 
    year_disestablished INTEGER, 
    month_disestablished TEXT, 
    day_disestablished INTEGER,
    country_id INTEGER
);
'''
