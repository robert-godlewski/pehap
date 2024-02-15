# Grabs all of the locations necessary within the USA
from urllib.request import urlopen
from bs4 import BeautifulSoup
from linkfinder import findLink
from find_admin_divisions import findDivisions
from enviornment_variables import wiki, countries_table, admin_divisions_table
from location import Country, AdminDivision

import ssl
import sqlite3


# Ignore SSL certificate errors since we are using Wikipedia for this
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Creating out Database if needed
con = sqlite3.connect('sql.db')
cur = con.cursor()
cur.executescript(countries_table)
cur.executescript(admin_divisions_table)

parser = 'html.parser'

# wiki = 'https://en.wikipedia.org/'
url = wiki + 'wiki/United_States'
# url = input('Enter wiki page: ')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, parser)

# Here and below only works for the USA - Possibly fix later on
# print(soup.title)
# usa_info = soup.find_all('td', 'infobox-data')
# print(f'USA Info : {usa_info}')
# print(f'Size of list: {len(usa_info)}')
# Administrative regions within the USA that works
usa_admin_divisions = findLink(soup, title='List of states and territories of the United States')
admin_url = wiki + 'wiki/' + usa_admin_divisions
# print(f'Current Divisions Link = {admin_url}')
# Might need later but these territories might not have representation in the USA congress
usa_territory_history = findLink(soup, title='Territorial evolution of the United States')
territory_history_url = wiki + 'wiki/' + usa_territory_history
# print(f'Territorial History of the USA Link = {territory_history_url}')

# Adding in USA to countries table if needed
have_usa = False
usa = None
# usa_raw = None
usa_name = 'United States of America'

# This while loop works
# while not have_usa:
#     cur.execute("SELECT * FROM countries WHERE name = ? ", (memoryview(usa_name.encode()),))
#     usa_raw = cur.fetchone()
#     if usa_raw:
#         # print(usa_raw)
#         print('Already have this in the Database')
#         have_usa = True
#     else:
#         # print('Need to add it in')
#         cur.execute('''INSERT INTO countries (name, links, year_established, month_established, day_established) VALUES ( ?, ?, ?, ?, ? )''', (memoryview(usa_name.encode()), memoryview(f'{url} | {admin_url} | {territory_history_url}'.encode()), 1776, memoryview('July'.encode()), 4), )
#         con.commit()
#         print('Added the USA to the database')

# This stuff doesn't work yet
usa_list = Country.get_countries_by_name({'name': usa_name})
if len(usa_list) >= 1:
    if usa_list == 1:
        raw = usa_list[0]
        data = Country.convertRawData(raw)
        usa = Country(data)
    else:
        i = 0
        while i < len(usa_list):
            raw = usa_list[i]
            data = Country.convertRawData(raw)
            info = Country(data)
            if info.currently_around():
                usa = info
                i = len(usa_list)
            i += 1
else:
    links = f'{url} | {admin_url} | {territory_history_url}'
    data = {
        'name': memoryview(usa_name.encode()),
        'links': memoryview(links.encode()),
        'year_established': 1776,
        'month_established': memoryview('July'.encode()),
        'day_established': 4,
        'year_disestablished': None,
        'month_disestablished': None,
        'day_disestablished': None,
        'old_country_id': None
    }
    usa = Country.create_country(data)

# Adding in the USA admin divisions
# usa_data = {
#     "id": usa_raw[0],
#     "name": str(usa_raw[1],'utf-8'),
#     "links": str(usa_raw[2],'utf-8').split(" | "),
#     "year_established": usa_raw[3],
#     "month_established": str(usa_raw[4],'utf-8'),
#     "day_established": usa_raw[5]
# }
# usa = Country(usa_data)
# usa = Country(usa_raw)
print(f"USA: {usa}")

admin_html = urlopen(url=admin_url, context=ctx).read()
admin_soup = BeautifulSoup(admin_html, parser)
# fix this function to also save in the DB
regions = findDivisions(admin_soup)
# print(f'Regions List = {regions}')
for region in regions:
    cur.execute("SELECT * FROM admin_divisions WHERE name = ? ", (memoryview(region['name'].encode()),))
    region_raw = cur.fetchone()
    if region_raw:
        print(region_raw)
        print('Already have this in the Database')
    else:
        cur.execute("INSERT INTO admin_divisions (name, links, country_id) VALUES ( ?, ?, ? )", (memoryview(region['name'].encode()), memoryview(region['links'].encode()), usa.id), )
        con.commit()
        print(f'Added in a new region to the database: {region}')

con.close()
