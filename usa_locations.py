# Grabs all of the locations necessary
# References: https://beautiful-soup-4.readthedocs.io/en/latest/
from urllib.request import urlopen
from bs4 import BeautifulSoup
from linkfinder import findLink
from find_admin_divisions import findDivisions

import ssl
import sqlite3


# Ignore SSL certificate errors since we are using Wikipedia for this
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Creating out Database
# con = sqlite3.connect('sql.db')
# cur = con.cursor()
# cur.execute('''CREATE TABLE IF NOT EXISTS countries (name TEXT, links TEXT, year_established INTEGER, month_established TEXT, day_established INTEGER, year_disestablished INTEGER, month_disestablished TEXT, day_disestablished INTEGER)''')


# fix below
wiki = 'https://en.wikipedia.org'
url = wiki + '/wiki/United_States'
# url = input('Enter wiki page: ')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Here and below only works for the USA - Possibly fix later on
# print(soup.title)
# usa_info = soup.find_all('td', 'infobox-data')
# print(f'USA Info : {usa_info}')
# print(f'Size of list: {len(usa_info)}')
usa_admin_divisions = findLink(soup, title='List of states and territories of the United States')
admin_url = wiki + '/wiki/' + usa_admin_divisions
# print(f'Current Divisions Link = {admin_url}')
# Might need later but these territories might not have representation in the USA congress
usa_territory_history = findLink(soup, title='Territorial evolution of the United States')
territory_history_url = wiki + '/wiki/' + usa_territory_history
# print(f'Territorial History of the USA Link = {territory_history_url}')

# Adding in USA to countries table
# cur.execute('''INSERT INTO countries (name, links, year_established, month_established, day_established) VALUES ( ?, ?, ?, ?, ? )''', (memoryview('United States of America'.encode()), memoryview(f'{url} | {admin_url} | {territory_history_url}'.encode()), 1776, memoryview('July'.encode()), 4), )
# con.commit()

# Adding in the USA admin divisions
admin_html = urlopen(url=admin_url, context=ctx).read()
admin_soup = BeautifulSoup(admin_html, 'html.parser')
# fix this function to also save in the DB
regions = findDivisions(admin_soup)
print(f'Regions List = {regions}')

# con.close()
