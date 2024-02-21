# Grabs all of the locations necessary within the USA
from urllib.request import urlopen
from bs4 import BeautifulSoup
from linkfinder import findLink
from find_admin_divisions import findDivisions
from enviornment_variables import db_name, wiki, countries_table, admin_divisions_table
from location import Country, AdminDivision

import ssl
import sqlite3


# Ignore SSL certificate errors since we are using Wikipedia for this
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Creating out Database if needed
con = sqlite3.connect(db_name)
cur = con.cursor()
cur.executescript(countries_table)
cur.executescript(admin_divisions_table)

parser = 'html.parser'

url = wiki + '/wiki/United_States'
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
admin_url = wiki + '/wiki/' + usa_admin_divisions
# print(f'Current Divisions Link = {admin_url}')
# Might need later but these territories might not have representation in the USA congress
usa_territory_history = findLink(soup, title='Territorial evolution of the United States')
territory_history_url = wiki + '/wiki/' + usa_territory_history
# print(f'Territorial History of the USA Link = {territory_history_url}')

# Adding in USA to countries table if needed
usa_name = 'United States of America'
usa_dict = {
    'name': usa_name,
    'links': [url,admin_url,territory_history_url],
    'year_established': 1776,
    'month_established': 'July',
    'day_established': 4
}
usa = Country(usa_dict)
usa_list = None
while not usa_list:
    usa_list = usa.get_countries_by_name(usa_dict)
    # print(usa_list)
    if len(usa_list) >= 1:
        if len(usa_list) > 1:
            # print("Finding the most current one")
            for i in usa_list:
                # print(i)
                temp = usa.convertRawData(i)
                # print(temp)
                if 'year_disestablished' not in temp: data = temp
        else:
            # print("We have one to save to usa object")
            data = usa.convertRawData(usa_list[0])
        usa = Country(data)
        # print("Updated usa object")
    else:
        usa.create_country(usa_dict)
        usa_list = None

print(f"USA id = {usa.id}")
print(f"USA name = {usa}")
print(f"USA links = {usa.links}")
print(f"USA date established = {usa.month_established} {usa.day_established}, {usa.year_established}")

admin_html = urlopen(url=admin_url, context=ctx).read()
admin_soup = BeautifulSoup(admin_html, parser)
regions = findDivisions(admin_soup)
# print(f'Regions List = {regions}')
for region_data in regions:
    region_data['country_id'] = usa.id
    print(f'region = {type(region_data)} {region_data}')
    region = AdminDivision(region_data)
    region_list = None
    while not region_list: 
        region_list = region.get_admin_divs_by_name(region_data)
        # print(region_list)
        if len(region_list) >= 1:
            if len(region_list) > 1:
                # print("Finding the most current one")
                for i in region_list:
                    # print(i)
                    temp = region.convertRawData(i)
                    # print(temp)
                    if 'year_disestablished' not in temp: data = temp
            else:
                # print("We have one to save to admin object")
                data = region.convertRawData(region_list[0])
            region = AdminDivision(data)
            # print("Updated admin object")
        else:
            region.create_admin_div(region_data)
            region_list = None

con.close()
