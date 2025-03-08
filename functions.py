# Contains some helper functions to use to help convert data
from models import ElectionYear


def strToIntComplex(strnum: str) -> int:
    # Converts large numbers like 1,000,000 from a string to a number
    num_arr = strnum.split(",")
    num = 0
    i = len(num_arr)-1
    multi = 1
    while i >= 0:
        temp = int(num_arr[i])
        temp_mult = temp * multi
        num += (temp_mult-temp)
        i -= 1
        multi += 1000
    return num

def handleData(db_name: str, raw_data: list) -> None:
    # Helper function to go through the raw_data and save it to a sql db via db_name
    # This is the initial data that we need to properly save the data to the db
    election_year = raw_data[0]
    party = raw_data[1]
    president_name = raw_data[2]
    vice_president_name = raw_data[3]
    popular_vote = strToIntComplex(raw_data[4])
    total_population = strToIntComplex(raw_data[5])
    # We don't need to save raw_data[6] because we can just calculate this later
    electoral_vote = raw_data[7]
    total_electoral = raw_data[8]
    # We don't need to save raw_data[9] because we can just calculate this later
    notes = raw_data[10]
    won = raw_data[11]
    ElectionYear.createEY({
        'year': election_year,
        'total_population': total_population,
        'total_electoral': total_electoral
    })
    year_data = ElectionYear.getEYbyYear({'year': election_year})
    # add in the different classes to convert the information above into this...

# Old information to add into handleData()
# from db import DB
# def handleData(raw_data: list) -> None:
#     office_data = [
#         working_db.createOrGetOfficePosition('President'),
#         working_db.createOrGetOfficePosition('Vice President')
#     ]
#     data = [... for i in raw_data]
#     party_data = working_db.createOrGetParty(data)
#     president_data = working_db.createOrGetCandidate(data,'president_name')
#     working_db.createCandidateElection(data, year_data, president_data)
#     working_db.createCandidateParty(candidate_id=president_data['id'], party_id=party_data['id'])
#     working_db.createCandidateOffice(candidate_id=president_data['id'], office_id=office_data[0]['id'])
#     vice_president_data = working_db.createOrGetCandidate(data,'vice_president_name')
#     working_db.createCandidateElection(data, year_data, vice_president_data)
#     working_db.createCandidateParty(candidate_id=vice_president_data['id'], party_id=party_data['id'])
#     working_db.createCandidateOffice(candidate_id=vice_president_data['id'], office_id=office_data[1]['id'])
# working_db.deactivate()