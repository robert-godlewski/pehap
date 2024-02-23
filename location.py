# Todo: need to add in db SQL scripts in these
# This is a group of models to interface with the db for locations
# Contains Country and AdminDivision
from enviornment_variables import db_name

import sqlite3


con = sqlite3.connect(db_name)
cur = con.cursor()


# This is a model format for regions
class Location:
    def __init__(self, data: dict) -> None:
        if 'id' in data: self.id = data['id']
        else: self.id = None
        self.name = data['name']
        if 'links' in data: self.links = data['links']
        else: self.links = None
        ye = 'year_established'
        if ye in data: self.year_established = data[ye]
        else: self.year_established = None
        me = 'month_established'
        if me in data: self.month_established = data[me]
        else: self.month_established = None
        de = 'day_established'
        if de in data: self.day_established = data[de]
        else: self.day_established = None
        yd = 'year_disestablished'
        if yd in data: self.year_disestablished = data[yd]
        else: self.year_disestablished = None
        md = 'month_disestablished'
        if md in data: self.month_disestablished = data[md]
        else: self.month_disestablished = None
        dd = 'day_disestablished'
        if dd in data: self.day_disestablished = data[dd]
        else: self.day_disestablished = None

    def __str__(self) -> str: return self.name

    def currently_around(self) -> bool:
        # determined if the country is still around or not
        if self.year_disestablished: return False
        else: return True


class Country(Location):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        if 'old_country_id' in data: self.old_country_id = data['old_country_id']
        else: self.old_country_id = None

    @classmethod
    def create_country(cls, data: dict) -> None:
        # print(f'data in = {type(data)} {data}')
        name = None
        if 'name' in data: name = memoryview(data['name'].encode())
        links = None
        if 'links' in data:
            links_raw = ''
            for i in range(len(data['links'])):
                links_raw += data['links'][i]
                if i != len(data['links'])-1:
                    links_raw += ' | '
            links = memoryview(links_raw.encode())
        ye = None
        if 'year_established' in data: ye = data['year_established']
        me = None
        if 'month_established' in data: me = memoryview(data['month_established'].encode())
        de = None
        if 'day_established' in data: de = data['day_established']
        yd = None
        if 'year_disestablished' in data: yd = data['year_disestablished']
        md = None
        if 'month_disestablished' in data:
            md = memoryview(data['month_disestablished'].encode())
        dd = None
        if 'day_disestablished' in data: dd = data['day_disestablished']
        ocid = None
        if 'old_country_id' in data: ocid = data['old_country_id']
        cur.execute('''INSERT INTO countries (name, links, year_established, month_established, day_established, year_disestablished, month_disestablished, day_disestablished, old_country_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (name,links,ye,me,de,yd,md,dd,ocid,),)
        con.commit()
        # print(f'Added {data["name"]} to the database')

    @classmethod
    def get_country_by_id(cls, data: dict):
        cur.execute("SELECT * FROM countries WHERE id = ? ", data["id"], )
        country_raw = cur.fetchone()
        # print(f'Got = {country_raw}')
        return cls(country_raw)

    @classmethod
    def get_countries_by_name(cls, data: dict) -> list:
        cur.execute("SELECT * FROM countries WHERE name = ? ", (memoryview(data['name'].encode()),),)
        return cur.fetchall()

    @staticmethod
    def convertRawData(data: tuple) -> dict:
        # Converts data from db to a readable hash map
        # print(f'data converting: {data}')
        decodeType = 'utf-8'
        me = None
        if data[4]: me = str(data[4],decodeType)
        md = None
        if data[7]: md = str(data[7],decodeType)
        return {
            'id': data[0],
            'name': str(data[1],decodeType),
            'links': str(data[2],decodeType).split(" | "),
            'year_established': data[3],
            'month_established': me,
            'day_established': data[5],
            'year_disestablished': data[6],
            'month_disestablished': md,
            'day_disestablished': data[8],
            'old_country_id': data[9]
        }


class AdminDivision(Location):
    # Model for Administrative Divisions
    # States, Provinces, Territories, etc are considered to be in this category
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        if 'country_id' in data: self.country_id = data['country_id']
        else: self.country_id = None
        if 'title' in data: self.title = data['title']
        else: self.title = None
        if 'old_admin_id' in data: self.old_admin_id = data['old_admin_id']
        else: self.old_admin_id = None

    def __str__(self) -> str:
        if self.title is not None: return f'The {self.title} of {self.name}'
        else: return super().__str__()

    @classmethod
    def create_admin_div(cls, data: dict) -> None:
        # print(f'data in = {type(data)} {data}')
        name = None
        if 'name' in data: name = memoryview(data['name'].encode())
        links = None
        if 'links' in data:
            links_raw = ''
            for i in range(len(data['links'])):
                links_raw += data['links'][i]
                if i != len(data['links'])-1:
                    links_raw += ' | '
            links = memoryview(links_raw.encode())
        ye = None
        if 'year_established' in data: ye = data['year_established']
        me = None
        if 'month_established' in data: me = memoryview(data['month_established'].encode())
        de = None
        if 'day_established' in data: de = data['day_established']
        yd = None
        if 'year_disestablished' in data: yd = data['year_disestablished']
        md = None
        if 'month_disestablished' in data:
            md = memoryview(data['month_disestablished'].encode())
        dd = None
        if 'day_disestablished' in data: dd = data['day_disestablished']
        cid = None
        if 'country_id' in data: cid = data['country_id']
        title = None
        if 'title' in data: title = memoryview(data['title'].encode())
        oaid = None
        if 'old_admin_id' in data: oaid = data['old_admin_id']
        cur.execute('''INSERT INTO admin_divisions (name, links, year_established, month_established, day_established, year_disestablished, month_disestablished, day_disestablished, country_id, title, old_admin_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (name,links,ye,me,de,yd,md,dd,cid,title,oaid,),)
        con.commit()
        # print(f'Added {data["name"]} to the database')

    @classmethod
    def get_admin_divs_by_id(cls, data: dict):
        cur.execute("SELECT * FROM admin_divisions WHERE id = ? ", data["id"], )
        admin = cur.fetchone()
        # print(f'Got = {admin}')
        return cls(admin)

    @classmethod
    def get_admin_divs_by_name(cls, data: dict) -> list:
        cur.execute("SELECT * FROM admin_divisions WHERE name = ? ", (memoryview(data['name'].encode()),),)
        return cur.fetchall()

    @classmethod
    def get_admin_divs_by_country_id(cls, data: dict) -> list:
        cur.execute("SELECT * FROM admin_divisions WHERE country_id = ? ", (data['country_id'],),)
        # all_divs = cur.fetchall()
        # print(f'Found: {all_divs}')
        # return all_divs
        return cur.fetchall()

    @staticmethod
    def convertRawData(data: tuple) -> dict:
        # Converts data from db to a readable hash map
        # print(f'data converting: {data}')
        decodeType = 'utf-8'
        me = None
        if data[4]: me = str(data[4],decodeType)
        md = None
        if data[7]: md = str(data[7],decodeType)
        title = None
        if data[10]: title = str(data[10],decodeType)
        return {
            'id': data[0],
            'name': str(data[1],decodeType),
            'links': str(data[2],decodeType).split(" | "),
            'year_established': data[3],
            'month_established': me,
            'day_established': data[5],
            'year_disestablished': data[6],
            'month_disestablished': md,
            'day_disestablished': data[8],
            'country_id': data[9],
            'title': title,
            'old_admin_id': data[11]
        }
