# Grabs all of the locations necessary within the USA
from urllib.request import urlopen
from bs4 import BeautifulSoup
from linkfinder import findLink
from find_admin_divisions import findDivisions
from enviornment_variables import wiki

import ssl
import sqlite3


# Ignore SSL certificate errors since we are using Wikipedia for this
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Creating out Database if needed
con = sqlite3.connect('sql.db')
cur = con.cursor()
cur.executescript('''
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    name TEXT, 
    links TEXT, 
    year_established INTEGER, 
    month_established TEXT, 
    day_established INTEGER, 
    year_disestablished INTEGER, 
    month_disestablished TEXT, 
    day_disestablished INTEGER
);
''')

'''
CREATE TABLE IF NOT EXISTS admin_divisions (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    name TEXT, 
    links TEXT, 
    year_established INTEGER, 
    month_established TEXT, 
    day_established INTEGER, 
    year_disestablished INTEGER, 
    month_disestablished TEXT, 
    day_disestablished INTEGER,
    country_id INTEGER
);
'''#)


# wiki = 'https://en.wikipedia.org/'
url = wiki + 'wiki/United_States'
# url = input('Enter wiki page: ')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Here and below only works for the USA - Possibly fix later on
# print(soup.title)
# usa_info = soup.find_all('td', 'infobox-data')
# print(f'USA Info : {usa_info}')
# print(f'Size of list: {len(usa_info)}')
# More refined links for administrative regions within the USA
usa_states_raw = findLink(soup, title='U.S. state')
usa_states_url = wiki + 'wiki/' + usa_states_raw
usa_territories_raw = findLink(soup, title='Territories of the United States')
usa_territories_url = wiki + 'wiki/' + usa_territories_raw
# Old administrative regions within the USA that works
# usa_admin_divisions = findLink(soup, title='List of states and territories of the United States')
# admin_url = wiki + 'wiki/' + usa_admin_divisions
# print(f'Current Divisions Link = {admin_url}')
# Might need later but these territories might not have representation in the USA congress
usa_territory_history = findLink(soup, title='Territorial evolution of the United States')
territory_history_url = wiki + 'wiki/' + usa_territory_history
# print(f'Territorial History of the USA Link = {territory_history_url}')

# Adding in USA to countries table if needed
cur.execute("SELECT * FROM countries WHERE name = ? ", (memoryview('United States of America'.encode()),))
usa = cur.fetchone()
if usa:
    print(usa)
    print('Already have this in the Database')
else:
    # print('Need to add it in')
    cur.execute('''INSERT INTO countries (name, links, year_established, month_established, day_established) VALUES ( ?, ?, ?, ?, ? )''', (memoryview('United States of America'.encode()), memoryview(f'{url} | {usa_states_url} | {usa_territories_url} | {territory_history_url}'.encode()), 1776, memoryview('July'.encode()), 4), )
    con.commit()
    print('Added the USA to the database')

# Adding in the USA admin divisions
# Might need to do something special here instead:
# * https://en.wikipedia.org/wiki/U.S._state
# * https://en.wikipedia.org/wiki/Territories_of_the_United_States
# Using these links might be a little simpler to parse through and we can do a separation of States and Territories

# Old but works
# admin_html = urlopen(url=admin_url, context=ctx).read()
# admin_soup = BeautifulSoup(admin_html, 'html.parser')
# fix this function to also save in the DB
# regions = findDivisions(admin_soup)
# print(f'Regions List = {regions}')

con.close()
