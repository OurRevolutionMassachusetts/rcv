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

also need to update the swap_cols attr

Sample usage for a vanilla RCV vote here:

```python3
from election.Election import Election

# In the source folder, put your CSV (with "unix" style line breaks), and provide relative path from 'source/'
source_file = '2018_gub/Final Valid Gubernatorial Endorsement Responses.csv'

# Election.timestamp_col: CSV column that indicates when vote was taken (default value is 'Timestamp')
# Election.voter_id: CSV column that marks the user's "unique id" (default value is 'Email address')
timestamp_col = 'Timestamp'
voter_id_col = 'Email address'

# The system is able to refer to a CSV file that lists all eligible voters. From there you can simply report on those
# that do no appear in the "registration" file, or run the results leaving those people out.
#
# This file should be placed somewhere in the "source" folder
registration_file = '/dir/filename.csv'   # where to find the file
registration_voterid_col = 'email'        # column that lists the "voter_id" for each registrant


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
e.registration_file = registration_file
e.registration_voterid_col = registration_voterid_col

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
e.second_ballot(knockout='Poseidon Earthshaker'))
```

Sample usage for a Scottish style STV vote here:

```python3
from election.ScottishStvElection import ScottishStvElection
import csv

# In the source folder, put your CSV (with "unix" style line breaks), and provide relative path from 'source/'
source_file = '2019_priorities/2019priorities.csv'

# Election.timestamp_col: CSV column that indicates when vote was taken (default value is 'Timestamp')
# Election.voter_id: CSV column that marks the user's "unique id" (default value is 'Email address')
timestamp_col = 'Timestamp'
voter_id_col = 'Email Address'

# The system is able to refer to a CSV file that lists all eligible voters. From there you can simply report on those
# that do no appear in the "registration" file, or run the results leaving those people out.
#
# This file should be placed somewhere in the "source" folder
registration_file = None   # where to find the file
registration_voterid_col = None        # column that lists the "voter_id" for each registrant

# columns holding the actual votes, and how to refer to them in results
# columns holding the actual votes, and how to refer to them in results
vote_cols = {
    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Affordable Housing (6)]": "Affordable Housing",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Climate Change/Green New Deal (15)]": "Climate Change/Green New Deal",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Democratic Party Transformation (5)]": "Democratic Party Transformation",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Fair Share Amendment/Millionaire's Tax (3)]": "Fair Share Amendment/Millionaire's Tax",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Good Jobs]": "Good Jobs",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Immigration (3)]": "Immigration",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Indigenous People/Nations (3)]": "Indigenous People/Nations",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Internal organizing: Build the number and strength of ORMA affiliates by facilitating sharing of best "
    "practices, engaging in community outreach, and addressing systemic structures of "
    "discrimination]": "Internal organizing",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Medicare for All/Single-payer Healthcare (13)]": "Medicare for All/Single-payer Healthcare",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Money out of Politics (9)]": "Money out of Politics",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Municipal Elections (7)]": "Municipal Elections",

    "After reviewing the detailed proposals, please rank the following priorities in order of preference for ORMA to "
    "apply it's resources. (That includes you! Our valuable volunteers.) Please work from 1st choice, up to 12th "
    "choice, selecting as many items as you like based on what YOU would like to work on: "
    "[Voting Reform - including Ranked Choice "
    "Voting & HR1 (10)]": "Voting Reform - including Ranked Choice Voting & HR1"
}

# voters that will fail "validation" but are known to be valid
whitelist = []

# order of the preference values
order = [
    '1st Choice',
    '2nd Choice',
    '3rd Choice'
]
for i in range(4,13):
    order.append(str(i) + 'th Choice')

# how many seats we're filling
seats = 5

# print out audit info
noisy = True

##############
# create the Election object and feed it basic data from above
# you should probably leave this section alone and skip to Execution below
##############

e = ScottishStvElection(order=order, seats=seats)
e.source_file = source_file
e.vote_cols = vote_cols
e.timestamp_col = timestamp_col
e.voter_id_col = voter_id_col
e.whitelist = whitelist
e.registration_file = registration_file
e.registration_voterid_col = registration_voterid_col
e.source_dir = '../source/'
e.noisy = noisy


##############
# Execution
##############

# load the csv into a data object and reset relevant attrs
#
# *drop_interlopers* allows you to kick out votes from people who don't appear in your registration data.
# if you want to run ballots both with and without unregistered voters, you'll need to run a separate bootstrap() for
# each scenario. Defaults to False.
#
# *cols_hold_prefs* background: the engine for loading votes assumes that the cols of the CSV hold the candidates, and
# the rows list the preference for each voter. Depending on how the ballot form is structured, data might come in with
# the preferences as column headers, and the candidates as values. For the latter case, set this value to True. Defaults
# to False.
e.bootstrap(drop_interlopers=False, cols_hold_prefs=False)

# e.registration_report()                     # prints out which voters were not registered

# run the first ballot and report results.
e.next_ballot()

# if we didn't have all needed winners, and there's no obvious knockout candidate, we redistribute the surplus votes
# for the choice with the most votes. if that's a tie, see
# https://blog.opavote.com/2016/11/plain-english-explanation-of-scottish.html
# for info on how to resolve.
# for now, manually supplying who should get knocked out or redistributed
# keep running next_ballot() with either subsequent redistribute or knockout args as needed
#
e.next_ballot(redistribute='Affordable Housing', knockout=None)
e.next_ballot(redistribute='Internal organizing', knockout=None)

# print out version of vote data with no voter info attached
e.redact(file='/Users/braiotta/Desktop/cd7 endorsement results for RC.csv')
```