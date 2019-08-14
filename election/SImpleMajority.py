from election.Election import Election
from sortedcontainers import SortedDict


class SimpleMajority(Election):

    def __init__(self, seats=None, **kwargs):
        Election.__init__(self, **kwargs)

    def record_votes(self, drop_interlopers=False):
        self.votes = {}
        if self.interlopers == []:
            self.find_interlopers()
        interlopers = [row[self.voter_id_col] for row in self.interlopers]

        for row in self.data:
            voter = row[self.voter_id_col]
            if drop_interlopers:
                if voter.lower() in interlopers:
                    print("!!! dropping vote cast by " + voter + " because they don't appear in the registration list")
                    continue

            # at this point we should record the vote
            for col_name, desc in self.vote_cols.items():
                vote = row[col_name].lower()
                if vote in ['yes', 'no']:
                    if desc not in self.votes:
                        self.votes[desc] = {"yes": 0, "no": 0}
                    self.votes[desc][vote] += 1

    def report(self):
        for desc, counts in self.votes.items():
            total_votes = counts['yes'] + counts['no']
            pct_yes = (counts['yes'] / total_votes) * 100

            if pct_yes > 50:
                print("** for " + desc + " with " + str(pct_yes) + "% voting yes we DO ENDORSE **")
            else:
                print("for " + desc + " with " + str(pct_yes) + "% voting yes we do not endorse")