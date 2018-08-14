import csv

class Election:
    def __init__(self, vote_cols=None, source_file=None, order=None, finish_line=60):
        self.data = None
        self.ballots_run = []
        self.finish_line = finish_line
        self.knockouts = []
        self.order = order
        self.registration_data = []
        self.registration_file = None
        self.registration_voterid_col = 'email'
        self.results = {}
        self.source_dir = './source/'
        self.source_file = source_file
        self.timestamp_col = 'Timestamp'
        self.vote_cols = vote_cols
        self.vote_count = 0
        self.voter_id_col = 'Email Address'
        self.votes = []

        if self.order is None:
            self.order = ['First Preference', 'Second Preference', 'Third Preference']

    def bootstrap(self):
        self.ballots_run = []
        self.knockouts = []
        self.data = list(csv.DictReader(open(self.source_dir + self.source_file)))
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
            print(new_row)
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

    # for easy extraction, for each voter construct an array in order of preferences
    def record_votes(self):
        for row in self.data:
            vote_dict = {}
            vote = []

            # create a key/value dict based on first pref/second pref/etc
            for col, shortname in self.vote_cols.items():
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