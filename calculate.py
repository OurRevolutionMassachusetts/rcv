from election.Election import Election

source_file = '2018_gub/Final Valid Gubernatorial Endorsement Responses.csv'

# name of the columns holding the actual votes, and how to refer to them in results
vote_cols = {
    'Select your preference for ORMA gubernatorial endorsement. [Bob Massie]':      'Bob Massie',
    'Select your preference for ORMA gubernatorial endorsement. [Jay Gonzalez]':    'Jay Gonzalez',
    'Select your preference for ORMA gubernatorial endorsement. [No Endorsement]':  'No Endorsement'
}

# create the Election object and feed it basic data
e = Election(source_file=source_file, vote_cols=vote_cols)

# load the file into a csv and reset relevant attrs
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