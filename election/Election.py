import csv


class Election:
    def __init__(self, vote_cols=None, source_file=None, order=None, finish_line=60):
        self.data = None
        self.ballots_run = []
        self.finish_line = finish_line
        self.interlopers = []
        self.knockouts = []
        self.order = order
        self.registration_data = []
        self.registration_file = None
        self.registration_voterid_col = 'email'
        self.results = {}
        self.source_dir = './source/'
        self.source_file = source_file
        self.swap_cols = []
        self.timestamp_col = 'Timestamp'
        self.vote_cols = vote_cols
        self.vote_count = 0
        self.voter_id_col = 'Email Address'
        self.votes = []

        if self.order is None:
            self.order = ['First Preference', 'Second Preference', 'Third Preference']

    def bootstrap(self, swap_vote_cols=False):
        self.ballots_run = []
        self.knockouts = []
        self.data = list(csv.DictReader(open(self.source_dir + self.source_file)))
        self.data = self.preen_voter_ids(data=self.data, voter_id_col=self.voter_id_col)
        if swap_vote_cols:
            self.swap_vote_cols()
        self.vote_count = len(self.data)
        self.cleanup_unicode()
        self.dedupe()

        self.record_votes()

    def cleanup_unicode(self):
        count = 0
        for row in self.data:
            new_row = {}
            for k,v in row.items():
                if '\ufeff' in k:
                    k = k.replace(u'\ufeff', '')
                new_row[k] = v
            self.data[count] = new_row
            count += 1

    def dedupe(self):
        from dateutil.parser import parse

        vote_times = {}

        # construct key of voter and most recent timestamp
        for row in self.data:
            voter_id = row[self.voter_id_col]
            this_timestamp = row[self.timestamp_col]

            # If the user has an entry in vote times, compare timestamps. This one earlier? Skip to next row.
            if voter_id in vote_times:
                other_timestamp = vote_times[voter_id]
                this_t = parse(this_timestamp)
                other_t = parse(other_timestamp)
                if this_t < other_t:
                    next

            vote_times[voter_id] = this_timestamp

        new_data = []
        for row in self.data:
            voter_id = row[self.voter_id_col]
            this_timestamp = row[self.timestamp_col]
            winning_timestamp = vote_times[voter_id]
            if this_timestamp == winning_timestamp:
                new_data.append(row)

        self.data = new_data

    def find_interlopers(self):
        # take our registration data and build a simple list of registered voter ids
        registered_ids = [row[self.registration_voterid_col] for row in self.registration_data]

        self.interlopers = []
        for row in self.data:
            if row[self.voter_id_col] not in registered_ids:
                self.interlopers.append(row)

    def first_ballot(self, drop_interlopers=False):
        self.results = {v: 0 for (k, v) in self.vote_cols.items()}

        # for the first ballot, we simply record everyone's first choice
        for row in self.votes:
            if row[0]:
                self.results[row[0]] += 1

        self.ballots_run.append('first')
        self.report()

    def load_registration(self):
        self.registration_data = list(csv.DictReader(open(self.source_dir + self.registration_file)))
        self.registration_data = self.preen_voter_ids(data=self.registration_data,
                                                      voter_id_col=self.registration_voterid_col)

    # for easy extraction, for each voter construct an array in order of preferences
    def record_votes(self):
        for row in self.data:
            vote_dict = {}
            vote = []

            # create a key/value dict based on first pref/second pref/etc
            for col, shortname in self.vote_cols.items():
                if col in row:
                    choice = row[col]
                    if choice:
                        vote_dict[choice] = shortname

            # use that dict to construct a simple ordered list of the user's choices
            for col in self.order:
                if col in vote_dict:
                    vote.append(vote_dict[col])
                else:
                    vote.append(None)

            self.votes.append(vote)

    def registration_report(self):
        if self.interlopers == []:
            self.find_interlopers()
        print(*(row[self.voter_id_col] for row in self.interlopers), sep='\n')

    def report(self):
        ballot_name = self.ballots_run[-1] + ' ballot'
        print(ballot_name)
        print('--------')

        for choice, raw in self.results.items():
            percentage = round(((raw / self.vote_count) * 100), 2)

            winner = ''
            if percentage >= self.finish_line:
                winner = ' ** WINNER **'

            print(choice + ': ' + str(raw) + ' (' + str(percentage) + '% of ' + str(self.vote_count) + ')' + winner)

    # this code was built expecting that the results CSV would have the candidate listed as the column, and the
    # preference listed as the value in the row. For cases where that's been reversed, this normalizes our data to work
    # with the logic as it exists.
    def swap_vote_cols(self):
        new_data = []

        for row in self.data:
            new_row = {}
            for k,v in row.items():
                if k in self.swap_cols:
                    if v:
                        new_row[v] = k
                else:
                    new_row[k] = v
            new_data.append(new_row)

        self.data = new_data

    @staticmethod
    def preen_voter_ids(data, voter_id_col):
        count = 0
        for row in data:
            data[count][voter_id_col] = str(data[count][voter_id_col]).lower()
            count += 1
        return data