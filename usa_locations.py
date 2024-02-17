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
usa_name = 'United States of America'
usa_temp = Country({
    'name': usa_name,
    'links': [url, admin_url, territory_history_url]
})
usa = None
usa_list = usa_temp.get_countries_by_name(usa_temp.name)
print(usa_list)
if len(usa_list) == 0:
    links = ''
    i = 0
    while i < len(usa_temp.links):
        links += usa_temp.links[i]
        if i != len(usa_temp.links)-1:
            links += ' | '
        i += 1
    data = {
        'name': memoryview(usa_temp.name.encode()),
        'links': memoryview(links.encode()),
        'year_established': 1776,
        'month_established': memoryview('July'.encode()),
        'day_established': 4,
        'year_disestablished': None,
        'month_disestablished': None,
        'day_disestablished': None,
        'old_country_id': None
    }
    usa = usa_temp.create_country(data)
elif len(usa_list) == 1:
    data = usa_temp.convertRawData(usa_list[0])
    usa = Country(data)
elif len(usa_list) > 1:
    i = 0
    while i < len(usa_list):
        raw = usa_list[i]
        data = usa_temp.convertRawData(usa_list[i])
        info = Country(data)
        if info.currently_around():
            usa = info
            i = len(usa_list)
        i += 1
print(f"USA: {usa}")

admin_html = urlopen(url=admin_url, context=ctx).read()
admin_soup = BeautifulSoup(admin_html, parser)
regions = findDivisions(admin_soup)
# print(f'Regions List = {regions}')
for region in regions:
    print(f'region = {type(region)} {region}')
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
