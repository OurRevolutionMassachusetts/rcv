from election.Election import Election

source_file = 'ORMA gubernatorial endorsement (Responses) - Form Responses 1.csv'

# name of the columns holding the actual votes, and how to refer to them in results
vote_cols = {
    'Select your preference for ORMA gubernatorial endorsement. [Bob Massie]':      'Bob Massie',
    'Select your preference for ORMA gubernatorial endorsement. [Jay Gonzalez]':    'Jay Gonzalez',
    'Select your preference for ORMA gubernatorial endorsement. [No Endorsement]':  'No Endorsement'
}

e = Election(source_file=source_file, vote_cols=vote_cols)