from election.Election import Election
from sortedcontainers import SortedDict

"""
when running a Scottish rules Single Transferable Vote Election
https://blog.opavote.com/2016/11/plain-english-explanation-of-scottish.html
"""


class ScottishStvElection(Election):
    def __init__(self, seats=None, **kwargs):
        self.excess_votes = {}
        self.multiplier = 1
        self.prior_winners = []
        self.redistributed_votes = []
        self.seats = seats
        self.threshold = None
        Election.__init__(self, **kwargs)

    def bootstrap(self, **kwargs):
        Election.bootstrap(self, **kwargs)
        self.derive_threshold()

    def derive_multiplier(self, choice):
        multiplier = 1

        # grab surplus and total for this choice
        excess = self.excess_votes[choice]
        if excess['excess'] > 0:
            multiplier = round(excess['excess'] / excess['total'], 5)

        if self.noisy:
            print()
            print('multiplier set for ' + choice + ' excess votes to ' + str(multiplier) + ' (' +
                  str(excess['excess']) + ' excess votes divided by ' + str(excess['total']) + ' total)')

        self.multiplier = multiplier
        return multiplier

    def derive_threshold(self):
        self.threshold = int((self.vote_count / (self.seats + 1)) + 1)
        return self.threshold

    def handle_excess_votes(self, raw_count, choice):
        excess = round(raw_count - self.threshold, 5)
        if excess > 0 and choice not in self.excess_votes:
            self.excess_votes[choice] = {'excess': excess, 'total': raw_count, 'used': False}
        return excess

    def next_ballot(self, redistribute=None, knockout=None):
        if redistribute and knockout:
            raise ValueError("can't run a ScottishStvElection.next_ballot() with both a redistribute and knockout")

        if not redistribute and not knockout:
            # first ballot? treat it as a no-knockout knockout.
            if self.ballots_run == 0:
                self.next_ballot__knockout(knockout=None)
            # otherwise, barf
            else:
                raise ValueError("can't run an additional ScottishStvElection.next_ballot() without a redistribution "
                                 "or a knockout")

        if redistribute:
            self.next_ballot__redistribute(redistribute_from=redistribute)

        if knockout:
            self.next_ballot__knockout(knockout=knockout)

        self.ballots_run += 1
        self.report()

    def next_ballot__knockout(self, knockout=None):
        if not self.results:
            self.results = {v: 0 for (k, v) in self.vote_cols.items()}
        if knockout:
            self.knockouts.append(knockout)

        for row in self.votes:
            # if there are knockouts due to subsequent rounds of balloting, don't want to count them so all other prefs
            # get promoted
            new_row = [choice for choice in row if choice not in self.knockouts]
            row = new_row
            if row[0]:
                self.results[row[0]] += 1

    def next_ballot__redistribute(self, redistribute_from):
        self.redistribute_votes(redistribute_from=redistribute_from)

        if not self.results:
            self.results = {v: 0 for (k, v) in self.vote_cols.items()}

        for row in self.redistributed_votes:
            # if there are knockouts due to subsequent rounds of balloting, don't want to count them so all other prefs
            # get promoted
            new_row = [choice for choice in row if choice not in self.knockouts]
            row = new_row
            if row[0]:
                self.results[row[0]] += self.multiplier
                if self.noisy:
                    print("applying " + str(self.multiplier) + " to " + row[0])

    def redistribute_votes(self, redistribute_from):
        self.derive_multiplier(choice=redistribute_from)
        if self.noisy:
            print()
            print("redistributing votes for " + redistribute_from)

        self.redistributed_votes = []
        for voter_ballot in self.votes:
            new_voter_ballot = []

            # if the first choice for this voter is the choice we're redistributing...
            if voter_ballot[0] == redistribute_from:
                # keep lopping off the first element until the one that replaces it hasn't already won
                valid_winner = False
                new_voter_ballot = voter_ballot[1:]
                while not valid_winner:
                    # if the list is now length 0, we're done
                    if len(new_voter_ballot) == 0:
                        valid_winner = True

                    this_winner = new_voter_ballot[0]
                    if this_winner not in self.prior_winners:
                        valid_winner = True

                    else:
                        new_voter_ballot.pop(0)

                self.redistributed_votes.append(new_voter_ballot)

                if self.noisy:
                    print("redistributing from following:")
                    print(voter_ballot)
                    print("vote gets redistributed to " + str(new_voter_ballot[0]) + ' at value of ' + str(self.multiplier))
                    print()

        if self.noisy:
            print()

        self.excess_votes[redistribute_from]['used'] = True
        self.excess_votes[redistribute_from]['multiplier'] = self.multiplier

    def report(self):
        print()
        ballot_name = 'ballot #' + str(self.ballots_run)
        print(ballot_name)
        print("threshold is " + str(self.threshold))
        print('--------')

        report = []

        # any winners from prior rounds?
        for choice in self.prior_winners:
            used = ' UNUSED'
            if self.excess_votes[choice]['used']:
                used = ' used'
            print('WINNER FROM PREVIOUS BALLOT: ' + str(choice) + ' (' + str(self.excess_votes[choice]['excess']) +
                  used + ' excess votes)')

        for choice, raw in self.results.items():
            # if a "none" makes it in, skip
            if not choice:
                continue

            winner = ''
            if raw >= self.threshold:
                excess = self.handle_excess_votes(raw_count=raw, choice=choice)
                winner = ' ** WINNER ** with ' + str(excess) + ' excess votes'
                if choice not in self.prior_winners:
                    self.prior_winners.append(choice)
                if self.excess_votes[choice]['used']:
                    winner += ' (votes already redistributed)'

            report.append(
                (choice + ': ' + str(raw) + winner))

        report.sort()
        print(*(r for r in report), sep="\n")
        print()
        print(str(self.seats - len(self.prior_winners)) + " of " + str(self.seats) + " seats left to fill")
        print()

        # offer suggestions for next round if needed
        if len(self.prior_winners) < self.seats:
            candidates_by_tally = SortedDict({})
            for choice, raw in self.results.items():
                if raw not in candidates_by_tally:
                    candidates_by_tally[raw] = []
                candidates_by_tally[raw].append(choice)

            # also get prior winners with unused excess in there
            for choice in self.excess_votes:
                if not self.excess_votes[choice]['used']:
                    total = self.excess_votes[choice]['total']
                    if total not in candidates_by_tally:
                        candidates_by_tally[total] = []
                    candidates_by_tally[total].append(choice)

            min_val = list(candidates_by_tally.keys())[0]
            max_val = list(candidates_by_tally.keys())[-1]

            print('===============')
            print('SUGGESTIONS')
            print('===============')

            print("the following still have unused excess votes:")
            for e in self.excess_votes.keys():
                if not self.excess_votes[e]['used']:
                    callout = ''
                    if e in candidates_by_tally[max_val]:
                        callout = ' <---- max vote getter'
                    print('* ' + e + callout + ': ' + str(self.results[e]) + ' votes')
            print()

            if len(candidates_by_tally[min_val]) == 1:
                print("the obvious knockout candidate would be " + candidates_by_tally[min_val][0] + " with " +
                      str(min_val) + " votes")
            else:
                print("there is no obvious knockout candidate")

            print()
            print('===============')
            print('ballot #' + str(self.ballots_run) + ' complete')
            print('===============')

        else:
            print('===============')
            print('DONE')
            print('===============')