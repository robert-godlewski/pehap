# Todo: need to add in db SQL scripts in these
from enviornment_variables import db_name


# This is a model format for regions
class Location:
    def __init__(self, data: dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.links = data['links']
        if 'title' in data: self.title = data['title']
        else: self.title = None
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
        if self.title:
            return f'The {self.title} of {self.name}'
        else:
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


# Model for Administrative Divisions
# States, Provinces, Territories, etc are considered to be in this category
class AdminDivision(Location):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.country_id = data['country_id']
