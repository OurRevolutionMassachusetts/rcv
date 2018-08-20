import csv


class Election:
    def __init__(self, vote_cols=None, source_file=None, order=None, finish_line=60):
        self.data = None
        self.ballots_run = 0
        self.finish_line = finish_line
        self.interlopers = []
        self.knockouts = []
        self.order = order
        self.raw_vote_count = 0
        self.registration_data = []
        self.registration_file = None
        self.registration_voterid_col = 'email'
        self.results = {}
        self.source_dir = './source/'
        self.source_file = source_file
        self.swap_cols = []
        self.timestamp_col = 'Timestamp'
        self.whitelist = []
        self.vote_cols = vote_cols
        self.vote_count = 0
        self.voter_id_col = 'Email Address'
        self.votes = []

        if self.order is None:
            self.order = ['First Preference', 'Second Preference', 'Third Preference']

    def bootstrap(self, cols_hold_prefs=False, drop_interlopers=False):
        self.ballots_run = 0
        self.knockouts = []
        self.data = list(csv.DictReader(open(self.source_dir + self.source_file, 'U')))
        self.data = self.preen_voter_ids(data=self.data, voter_id_col=self.voter_id_col)
        if cols_hold_prefs:
            self.swap_vote_cols()
        self.raw_vote_count = len(self.data)
        self.cleanup_unicode()
        self.dedupe()

        if self.registration_file:
            self.load_registration()

        self.record_votes(drop_interlopers=drop_interlopers)
        self.vote_count = len(self.votes)

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
                    continue

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
        if type(self.whitelist) is not list:
            self.whitelist = []

        # take our registration data and build a simple list of registered voter ids
        registered_ids = [row[self.registration_voterid_col] for row in self.registration_data]

        self.interlopers = []
        for row in self.data:
            if row[self.voter_id_col] not in registered_ids and row[self.voter_id_col] not in self.whitelist:
                self.interlopers.append(row)

    def load_registration(self):
        self.registration_data = list(csv.DictReader(open(self.source_dir + self.registration_file, 'U')))
        self.registration_data = self.preen_voter_ids(data=self.registration_data,
                                                      voter_id_col=self.registration_voterid_col)

    def next_ballot(self, knockout=False):
        self.results = {v: 0 for (k, v) in self.vote_cols.items()}
        if knockout:
            self.knockouts.append(knockout)

        for row in self.votes:
            new_row = [choice for choice in row if (not choice or choice not in self.knockouts)]
            row = new_row
            if row[0]:
                self.results[row[0]] += 1

        self.ballots_run += 1
        self.report()

    # for easy extraction, for each voter construct an array in order of preferences
    def record_votes(self, drop_interlopers=False):
        interlopers = []
        if drop_interlopers:
            if self.interlopers == []:
                self.find_interlopers()
            interlopers = [row[self.voter_id_col] for row in self.interlopers]

        for row in self.data:
            # are we dropping this voter for being unregistered?
            if drop_interlopers:
                if row[self.voter_id_col] in interlopers:
                    print('!!! dropping vote for ' + row[self.voter_id_col] + ' (not registered)')
                    continue

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

        print(str(len(self.interlopers)) + " questionable voters")
        print(*(row[self.voter_id_col] for row in self.interlopers), sep='\n')

    def report(self):
        ballot_name = 'ballot #' + str(self.ballots_run)
        print(ballot_name)
        print('--------')

        report = []

        for choice, raw in self.results.items():
            percentage = round(((raw / self.vote_count) * 100), 2)

            winner = ''
            if percentage >= self.finish_line:
                winner = ' ** WINNER **'

            report.append((choice + ': ' + str(raw) + ' (' + str(percentage) + '% of ' + str(self.vote_count) + ')' + winner))

        report.sort()
        print(*(r for r in report), sep="\n")
        print()

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