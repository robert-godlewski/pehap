# Grabs all of the administrative divisions within a country and saves the links
# from urllib.request import urlopen
from bs4 import BeautifulSoup
from enviornment_variables import wiki

import ssl


# Ignore SSL certificate errors since we are using Wikipedia for this
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def findDivisions(soup: BeautifulSoup) -> list:
    # Scans the page for a list of locations and returns the array
    # print(soup.title)
    tables = soup.find_all('table', 'wikitable')
    regions = []
    for table in tables:
        # print(f'Table: {table}')
        # if table.tbody: print('Should parse through')
        # else: print('Skip this')
        for row in table.tbody:
            # print(f'Row: {row}')
            # print('------------------')
            region_name = None
            region_link = None
            try:
                # print(f'Row Head: {row.th}')
                if row.th.a:
                    # print(f'Row Head a tag: {row.th.a}')
                    region_name = row.th.a.contents[0]
                    # print(f'Region name = {region_name}')
                    region_link = wiki + row.th.a.attrs['href']
                    # print(f'Region Link = {region_link}')
                    # Special for USA
                    if region_name == 'postal abbreviation':
                        region_name = None
                        region_link = None
                # else: print('No a tag in the Row Header try again')
            except: 
                # print('Skipping Row Header')
                pass
            if region_name and region_link:
                regions.append({'name': region_name, 'link': region_link})
            # print('++++++++++++++')
        # print('#########')
    return regions
