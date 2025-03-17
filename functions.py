# Contains some helper functions to use to help convert data
from models import ElectionYear, PoliticalParty, OfficePosition, Candidates, CandidatesToElections, CandidatesToParty, CandidatesToOffice


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

def officeData(db_name: str, position: str) -> list:
    # This is to get [president_position, vice_president_position] data to use to handle the data
    handler = OfficePosition(db_name)
    handler.createOffice({'position': position})
    return handler.getOfficeByPosition({'position': position})

def handleData(db_name: str, raw_data: list) -> None:
    # Helper function to go through the raw_data and save it to a sql db via db_name
    president_position_data = officeData(db_name, 'President')
    vp_position_data = officeData(db_name, 'Vice President')
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
    ey_handler = ElectionYear(db_name)
    ey_handler.createEY({
        'year': election_year,
        'total_population': total_population,
        'total_electoral': total_electoral
    })
    year_data = ey_handler.getEYbyYear({'year': election_year})
    pp_handler = PoliticalParty(db_name)
    pp_handler.createParty({'party': party})
    party_data = pp_handler.getPartyByName({'party': party})
    candidate_handler = Candidates(db_name)
    candidate_handler.createCandidate({'name': president_name})
    president_data = candidate_handler.getCandidateByName({'name': president_name})
    candidate_handler.createCandidate({'name': vice_president_name})
    vp_data = candidate_handler.getCandidateByName({'name': vice_president_name})
    cToE_base = {
        'popular_vote': popular_vote,
        'electoral_vote': electoral_vote,
        'notes': notes,
        'won': won,
        'election_id': year_data['id'],
        'candidate_id': president_data['id']
    }
    cToE_handler = CandidatesToElections(db_name)
    cToE_handler.createCandidateToElection(cToE_base)
    cToE_base['candidate_id'] = vp_data['id']
    cToE_handler.createCandidateToElection(cToE_base)
    cToP_handler = CandidatesToParty(db_name)
    cToP_handler.createCandidateToParty({
        'candidate_id': president_data['id'],
        'party_id': party_data['id']
    })
    cToP_handler.createCandidateToParty({
        'candidate_id': vp_data['id'],
        'party_id': party_data['id']
    })
    cToOff_handler = CandidatesToOffice(db_name)
    cToOff_handler.createCandidateToOffice({
        'candidate_id': president_data['id'],
        'office_id': president_position_data['id']
    })
    cToOff_handler.createCandidateToOffice({
        'candidate_id': vp_data['id'],
        'office_id': vp_position_data['id']
    })
