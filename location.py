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
        self.id = data['id']
        self.name = data['name']
        self.links = data['links']
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

    def __str__(self) -> str:
        return self.name

    def currently_around(self) -> bool:
        # determined if the country is still around or not
        if self.year_disestablished:
            return False
        else:
            return True


class Country(Location):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        if 'old_country_id' in data: self.old_country_id = data['old_country_id']
        else: self.old_country_id = None

    @classmethod
    def create_country(cls, data: dict):
        cur.execute('''INSERT INTO countries (name, links, year_established, month_established, day_established, year_disestablished, month_disestablished, day_disestablished, old_country_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', data, )
        con.commit()
        print(f'Added {data["name"]} to the database')
        countries = cls.get_countries_by_name(data)
        if len(countries) < 1: 
            print('Something went wrong here')
            return False
        else:
            # Its going to be the last country because we just created it
            return cls(countries[len(countries)-1])

    @classmethod
    def get_country_by_id(cls, data: dict):
        cur.execute("SELECT * FROM countries WHERE id = ? ", data["id"], )
        country_raw = cur.fetchone()
        return cls(country_raw)

    @staticmethod
    def convertRawData(data: tuple) -> dict:
        decodeType = 'utf-8'
        return {
            'id': data[0],
            'name': str(data[1],decodeType),
            'links': str(data[2],decodeType).split(" | "),
            'year_established': data[3],
            'month_established': str(data[4],decodeType),
            'day_established': data[5],
            'year_disestablished': data[6],
            'month_disestablished': str(data[7],decodeType),
            'day_disestablished': data[8],
            'old_country_id': data[9]
        }

    @staticmethod
    def get_countries_by_name(data: dict) -> list:
        cur.execute("SELECT * FROM countries WHERE name = ? ", data["name"], )
        return cur.fetchall()


class AdminDivision(Location):
    # Model for Administrative Divisions
    # States, Provinces, Territories, etc are considered to be in this category
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.country_id = data['country_id']
        self.title = None
        if 'title' in data: 
            if type(data['title']) == str: self.title = data['title']
            else: self.title = str(data['title'],'utf-8')
        if 'old_admin_id' in data: self.old_admin_id = data['old_admin_id']
        else: self.old_admin_id = None

    def __str__(self) -> str:
        if self.title:
            return f'The {self.title} of {self.name}'
        else:
            return super().__str__()
