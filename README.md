Script for calculating RCV results, based on CSV file (in our case, drawn from Google forms).

*requires python3*

See calculate.py for sample usage. General sample usage here:

```python3
from election.Election import Election

# In the source folder, put your CSV (with "unix" style line breaks), and provide relative path from 'source/'
source_file = '2018_gub/Final Valid Gubernatorial Endorsement Responses.csv'

# columns holding the actual votes, and how to refer to them in results
vote_cols = {
    'Select your preference for the election. [Pheobus Apollo]':      'Phoebus Apollo',
    'Select your preference for the election. [Pallas Athene]':      'Pallas Athene',
    'Select your preference for the election. [Poseidon Earthshaker]':  'Poseidon Earthshaker'
}

# Election.timestamp_col: CSV column that indicates when vote was taken (default value is 'Timestamp')
# Election.voter_id: CSVcolumn that marks the user's "unique id" (default value is 'Email address')
e.timestamp_col = 'Timestamp'
e.voter_id_col = 'Email address'

# The system is able to refer to a CSV file that lists all eligible voters. From there you can simply report on those
# that do no appear in the "registration" file, or run the results leaving those people out.
#
# This file should be placed somewhere in the "source" folder
e.registration_file = '/dir/filename.csv'   # where to find the file
e.registration_voterid_col = 'email'        # column that lists the "voter_id" for each registrant
e.registration_report()                     # prints out which voters were not registered
e.first_ballot(drop_interlopers=True)       # runs ballot leaving out unregistered voters

# create the Election object and feed it basic data from above
e = Election(source_file=source_file, vote_cols=vote_cols)

# load the csv into a data object and reset relevant attrs
e.bootstrap()

# run the first ballot and report results.
e.first_ballot()

# run the second ballot
# haven't written this yet, but will go through all votes. for each one that had the knockout as first element in their
# vote list(), will take the second element and add to results and then see where we're at percentage-wise.
# e.second_ballot()

# run the third ballot
# haven't written this yet, also not sure what the right step is at this point.
# e.third_ballot()
```