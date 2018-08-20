Script for calculating RCV results, based on CSV file (in our case, drawn from Google forms).

*requires python3*

# Using the *cols_hold_prefs* arg to bootstrap():

Use *cols_hold_prefs=False* if your vote data looks like
```
email,candidate 1,candidate 2
bernie@ourrev.org,First Preference,Second Preference
```

Use *cols_hold_prefs=True* if your vote data looks like
```
email,First Preference,Second Preference
bernie@ourrev.org,candidate 1,candidate 2
```

Sample usage here:

```python3
from election.Election import Election

# In the source folder, put your CSV (with "unix" style line breaks), and provide relative path from 'source/'
source_file = '2018_gub/Final Valid Gubernatorial Endorsement Responses.csv'

# Election.timestamp_col: CSV column that indicates when vote was taken (default value is 'Timestamp')
# Election.voter_id: CSV column that marks the user's "unique id" (default value is 'Email address')
timestamp_col = 'Timestamp'
voter_id_col = 'Email address'

# columns holding the actual votes, and how to refer to them in results
vote_cols = {
    'Select your preference for the election. [Pheobus Apollo]':      'Phoebus Apollo',
    'Select your preference for the election. [Pallas Athene]':      'Pallas Athene',
    'Select your preference for the election. [Poseidon Earthshaker]':  'Poseidon Earthshaker'
}

# voters that will fail "validation" but are known to be valid
whitelist = [
    'heracles@crete.org',
    'jason@colchisgates.com'
]

##############
# end of values you normally need to update for each run
##############

# create the Election object and feed it basic data from above
e = Election()
e.source_file = source_file
e.vote_cols = vote_cols
e.timestamp_col = timestamp_col
e.voter_id_col = voter_id_col
e.whitelist = whitelist

# The system is able to refer to a CSV file that lists all eligible voters. From there you can simply report on those
# that do no appear in the "registration" file, or run the results leaving those people out.
#
# This file should be placed somewhere in the "source" folder
e.registration_file = '/dir/filename.csv'   # where to find the file
e.registration_voterid_col = 'email'        # column that lists the "voter_id" for each registrant

# load the csv into a data object and reset relevant attrs
#
# *drop_interlopers* allows you to kick out votes from people who don't appear in your registration data.
# if you want to run ballots both with and without unregistered voters, you'll need to run a separate bootstrap() for
# each scenario. Defaults to False
#
# *cols_hold_prefs* background: the engine for loading votes assumes that the cols of the CSV hold the candidates, and
# the rows list the preference for each voter. Depending on how the ballot form is structured, data might come in with
# the preferences as column headers, and the candidates as values. For the latter case, set this value to True. Defaults
#
e.bootstrap(drop_interlopers=True, cols_hold_prefs=False)

e.registration_report()                     # prints out which voters were not registered

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