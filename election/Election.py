class Election:
    def __init__(self, vote_cols=None, source_file=None, order=None, autoload=True):
        self.data = None
        self.order = order
        self.results = {}
        self.source_dir = './source/'
        self.source_file = source_file
        self.timestamp_col = 'Timestamp'
        self.vote_cols = vote_cols
        self.vote_count = 0
        self.votes = []

        if self.order is None:
            self.order = ['First Preference', 'Second Preference', 'Third Preference']

        if autoload and self.source_file and self.vote_cols:
            self.load_data()
            self.tabulate()

    def load_data(self):
        import csv
        self.votes = csv.DictReader(open(self.source_dir + self.source_file))

    def rank(self):
        for option, rankings in self.results.items():
            shortname = self.vote_cols[option]
            print('for option ' + shortname + ":")
            for place in self.order:
                percentage = (rankings[place] / self.vote_count) * 100
                print("\t" + place + ': ' + str(rankings[place]) + ' (' + str(round(percentage, 2)) + '% of ' + str(self.vote_count) +
                      ' votes cast)')
            print()

    def record_votes(self):
        # extract the rankings for the different options
        for vote in self.votes:
            self.vote_count += 1
            for col, shortname in self.vote_cols.items():
                pref = vote[col]
                if pref:
                    if pref not in self.results[col]:
                        self.results[col][pref] = 0
                    self.results[col][pref] += 1

    def tabulate(self):
        # bootstrap the results from vote_cols
        self.results = {k:{} for (k,v) in self.vote_cols.items()}
        self.vote_count = 0

        self.record_votes()
        # did the result meet the threshold
        self.rank()