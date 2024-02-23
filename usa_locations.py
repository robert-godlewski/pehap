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

# print(f"USA id = {usa.id}")
# print(f"USA name = {usa}")
# print(f"USA links = {usa.links}")
# print(f"USA date established = {usa.month_established} {usa.day_established}, {usa.year_established}")

admin_html = urlopen(url=admin_url, context=ctx).read()
admin_soup = BeautifulSoup(admin_html, parser)
regions = findDivisions(admin_soup)
# print(f'Regions List = {regions}')
for region_data in regions:
    region_data['country_id'] = usa.id
    # print(f'region = {type(region_data)} {region_data}')
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

# Here we are going to update the AdminDivisions with more complete information
blank_region = AdminDivision({'name': 'blank'})
usa_regions_raw = blank_region.get_admin_divs_by_country_id({'country_id': usa.id})
usa_regions = []
for region_raw in usa_regions_raw:
    # print(f'Raw regional data: {region_raw}')
    region_dict = blank_region.convertRawData(region_raw)
    region = AdminDivision(region_dict)
    print(f'Looking through: {region}')
    # Assuming that there's only one link
    region_html = urlopen(url=region.links[0], context=ctx).read()
    region_soup = BeautifulSoup(region_html, parser)
    # print(region_soup.title)
    tables = region_soup.find_all('table','infobox')
    for table in tables:
        for row in table.tbody:
            # print(f'Row: {row}')
            try:
                # print(row.td.div.contents)
                if row.td.div.a.contents[0] == 'State':
                    region.title = 'State'
                    print(f'{region.name} is a state')
                elif row.td.div.a.contents[0] == 'Unincorporated and unorganized U.S. territory' or row.td.div.a.contents[0] == 'Unincorporated and organized U.S. territory':
                    region.title = 'Territory'
                    print(f'{region.name} is a territory')
                elif row.td.div.contents[2].contents[0] == 'federal district':
                    region.title = 'Federal City'
                    print(f'{region.name} is a federal city')
            except: pass
            # try:
            #     # Skip the territories and the prior region for now
            #     if row.th.contents[0] == 'Before statehood': print(f'Need to add this to the db = {row.td.a.contents[0]}: {row.td.a.attrs["href"]}')
            # except: pass
            try:
                # Skip the territories for now
                if row.th.a.contents[0] == 'Admitted to the Union':
                    established_date_raw = row.td.contents[0]
                    established_date = established_date_raw.split(" ")
                    # Possible variations from this to fix:
                    # * ... Washington: ['November', '11,', '1889', '(42nd)'] -> ok but fix established_date[1]
                    # * ... West Virginia: ['June\xa020,', '1863'] -> the established_date[0] is weird
                    # * ... Wyoming: ['July', '10,', '1890'] -> ok but fix established_date[1]
                    if len(established_date) < 3:
                        # temp = established_date[0].split("xa")
                        # established_date[0] = temp[0]
                        # established_date.insert(1,temp[1])
                        print(f'bug: {established_date}')
                    if len(established_date) >=3:
                        # This should be done right after -> Remove the if statement after fixing the prior if statement
                        day_raw = established_date[1].split(",")
                        established_date[1] = int(day_raw[0])
                        year = int(established_date[2])
                        established_date[2] = year
                    # region.year_established = int(established_date[2])
                    # region.month_established = established_date[0]
                    # region.day_established = int(established_date[1])
                    print(f'Need to add in this established date to {region.name}: {established_date}')
            except: pass
            # Will need to copy above for Cities and Government Officials from the same table to add in later
            # print('===============')
    usa_regions.append(region)
# print(f'All regions: {usa_regions}')

con.close()
