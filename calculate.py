from election.Election import Election

registration_file = '2018_msex_da/middlesex an.csv'
source_file = '2018_msex_da/ORMA Middlesex DA Endorsement Poll (Responses) - Form Responses 1.csv'

# name of the columns holding the actual votes, and how to refer to them in results
vote_cols = {
    'Select your preference for ORMA gubernatorial endorsement. [Bob Massie]':      'Bob Massie',
    'Select your preference for ORMA gubernatorial endorsement. [Jay Gonzalez]':    'Jay Gonzalez',
    'Select your preference for ORMA gubernatorial endorsement. [No Endorsement]':  'No Endorsement'
}

# create the Election object and feed it basic data
e = Election()
e.source_file = source_file
e.vote_cols = vote_cols

# load list of registered voters
e.registration_file = registration_file
e.load_registration()


import sys
sys.exit(0)

# load the csv into a data object and reset relevant attrs
e.bootstrap()

# run the first ballot
e.first_ballot()

# run the second ballot
# haven't written this yet, but will go through all votes. for each one that had the knockout as first element in their
# vote list(), will take the second element and add to results and then see where we're at percentage-wise.
# e.second_ballot()

# run the third ballot
# haven't written this yet, also not sure what the right step is at this point.
# e.third_ballot()