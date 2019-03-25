import unittest
from unittest.mock import patch
from election.ScottishStvElection import ScottishStvElection


class ElectionTestCase(unittest.TestCase):
    @patch('election.Election.Election.__init__')
    def test_init(self, parent_init):
        e = ScottishStvElection(seats=5, anarg='whatever')
        self.assertEqual(e.seats, 5)
        self.assertEqual(e.multiplier, 1)

        args, kwargs = parent_init.call_args_list[0]
        self.assertEqual(kwargs, {'anarg': 'whatever'})

    @patch('election.ScottishStvElection.ScottishStvElection.derive_threshold')
    @patch('election.Election.Election.bootstrap')
    def test_bootstrap(self, bs, derive):
        e = ScottishStvElection(seats=5)
        e.bootstrap(anarg='whatever')
        args, kwargs = bs.call_args_list[0]
        self.assertEqual(kwargs, {'anarg': 'whatever'})

        self.assertTrue(derive.called)

    def test_derive_threshold(self):
        e = ScottishStvElection(seats=5)
        e.vote_count = 100
        self.assertEqual(17, e.derive_threshold())
        self.assertEqual(17, e.threshold)

        e = ScottishStvElection(seats=10)
        e.vote_count = 100
        self.assertEqual(10, e.derive_threshold())
        self.assertEqual(10, e.threshold)

    def test_handle_excess_votes(self):
        e = ScottishStvElection(seats=5)
        e.threshold = 10
        self.assertEqual(e.excess_votes, {})

        # excess votes to be reassigned later, this choice should appear in e.excess_votes
        excess = e.handle_excess_votes(raw_count=50, choice='more blood for oil')
        self.assertEqual(excess, 40)
        self.assertEqual(e.excess_votes, {'more blood for oil': {'excess': 40, 'total': 50, 'used': False}})

        # excess votes to be reassigned later, this choice should appear in e.excess_votes along with prior ones
        excess = e.handle_excess_votes(raw_count=15, choice='usa into nicaragua')
        self.assertEqual(excess, 5)
        self.assertEqual(e.excess_votes,{
            'more blood for oil': {'excess': 40, 'total': 50, 'used': False},
            'usa into nicaragua': {'excess': 5, 'total': 15, 'used': False}
        })

        # no excess votes to be reassigned later, this choice should NOT appear in e.excess_votes along with prior ones
        excess = e.handle_excess_votes(raw_count=10, choice='all the nukes')
        self.assertEqual(excess, 0)
        self.assertEqual(e.excess_votes, {
            'more blood for oil': {'excess': 40, 'total': 50, 'used': False},
            'usa into nicaragua': {'excess': 5, 'total': 15, 'used': False}
        })

        # testing negative value
        excess = e.handle_excess_votes(raw_count=1, choice='all the nukes')
        self.assertEqual(excess, -9)
        self.assertEqual(e.excess_votes, {
            'more blood for oil': {'excess': 40, 'total': 50, 'used': False},
            'usa into nicaragua': {'excess': 5, 'total': 15, 'used': False}
        })

    def test_derive_multiplier(self):
        e = ScottishStvElection(seats=5)
        self.assertEqual(1, e.multiplier)
        e.excess_votes = {
            'more blood for oil': {'excess': 40, 'total': 50, 'used': False},
            'usa into nicaragua': {'excess': 5, 'total': 15, 'used': False}
        }

        multiplier = e.derive_multiplier(choice='more blood for oil')
        self.assertEqual(multiplier, 0.8)
        self.assertEqual(e.multiplier, 0.8)

        multiplier = e.derive_multiplier(choice='usa into nicaragua')
        self.assertEqual(multiplier, 0.33333)
        self.assertEqual(e.multiplier, 0.33333)

    def test_redistribute_votes_results(self):
        e = ScottishStvElection(seats=5)
        e.excess_votes = {
            'Affordable Housing': {'excess': 4, 'total': 6, 'used': False}
        }

        e.votes = [
            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation', 
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations', 
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics', 
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],
            
            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation', 
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations', 
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],
            
            ['Internal organizing', 'Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration', 
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations', 
             None, None, None, None, None],
            
            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation', 
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations', 
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics', 
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],
            
            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation', 
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations', 
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],
            
            ['Internal organizing', 'Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration', 
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations', 
             None, None, None, None, None],
            
            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation', 
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations', 
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics', 
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],
            
            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation', 
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations', 
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],
            
            ['Internal organizing', 'Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration', 
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None]]

        # after redistributing, should have a new multiplier set, and votes with 'Affordable Housing' as first option
        # should now be on their second choice in e.redistributed votes
        e.redistribute_votes(redistribute_from='Affordable Housing')
        self.assertEqual(e.multiplier, 0.66667)
        self.assertEqual(e.redistributed_votes,
                         [
                             ['Climate Change/Green New Deal', 'Democratic Party Transformation',
                              "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration',
                              'Indigenous People/Nations',
                              'Internal organizing', 'Medicare for All/Single-payer Healthcare',
                              'Money out of Politics',
                              'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

                             ['Good Jobs', 'Democratic Party Transformation',
                              'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
                              'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None,
                              None],

                             ['Climate Change/Green New Deal', 'Democratic Party Transformation',
                              "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration',
                              'Indigenous People/Nations',
                              'Internal organizing', 'Medicare for All/Single-payer Healthcare',
                              'Money out of Politics',
                              'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

                             ['Good Jobs', 'Democratic Party Transformation',
                              'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
                              'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None,
                              None],

                             ['Climate Change/Green New Deal', 'Democratic Party Transformation',
                              "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration',
                              'Indigenous People/Nations',
                              'Internal organizing', 'Medicare for All/Single-payer Healthcare',
                              'Money out of Politics',
                              'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

                             ['Good Jobs', 'Democratic Party Transformation',
                              'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
                              'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None,
                              None]
                         ])

    def test_redistribute_votes_later_round_has_vote_for_user_that_has_already_won_but_has_others(self):
        e = ScottishStvElection(seats=5)
        e.excess_votes = {
            'Affordable Housing': {'excess': 4, 'total': 6, 'used': False},
            'Internal organizing': {'excess': 1, 'total': 3, 'used': False}
        }
        e.prior_winners = ['Affordable Housing', 'Internal organizing']
        e.ballots_run = 1

        e.votes = [
            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation',
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations',
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics',
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation',
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],

            ['Internal organizing', 'Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None],

            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation',
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations',
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics',
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation',
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],

            ['Internal organizing', 'Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None],

            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation',
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations',
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics',
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation',
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],

            ['Internal organizing', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None]]

        # in this example, 'Affordable Housing' has already won and been redistributed
        # we're now redistributing 'Internal organizing'
        # last of that choice's voters already chose 'Affordable Housing'
        # we should go down the user's list of priorities until we find one that hasn't won yet
        # but there isn't one
        e.redistribute_votes(redistribute_from='Internal organizing')
        self.assertEqual(e.redistributed_votes, [
            ['Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None],

            ['Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None],

            ['Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None]
        ])

    def test_redistribute_votes_later_round_has_vote_for_user_that_has_already_won_and_no_others(self):
        e = ScottishStvElection(seats=5)
        e.excess_votes = {
            'Affordable Housing': {'excess': 4, 'total': 6, 'used': False},
            'Internal organizing': {'excess': 1, 'total': 3, 'used': False}
        }
        e.prior_winners = ['Affordable Housing', 'Internal organizing']
        e.ballots_run = 1

        e.votes = [
            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation',
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations',
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics',
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation',
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],

            ['Internal organizing', 'Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None],

            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation',
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations',
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics',
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation',
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],

            ['Internal organizing', 'Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None],

            ['Affordable Housing', 'Climate Change/Green New Deal', 'Democratic Party Transformation',
             "Fair Share Amendment/Millionaire's Tax", 'Good Jobs', 'Immigration', 'Indigenous People/Nations',
             'Internal organizing', 'Medicare for All/Single-payer Healthcare', 'Money out of Politics',
             'Municipal Elections', 'Voting Reform - including Ranked Choice Voting & HR1'],

            ['Affordable Housing', 'Good Jobs', 'Democratic Party Transformation',
             'Medicare for All/Single-payer Healthcare', 'Indigenous People/Nations',
             'Voting Reform - including Ranked Choice Voting & HR1', None, None, None, None, None, None],

            ['Internal organizing', 'Affordable Housing', None, None, None, None, None, None, None, None, None]]

        # in this example, 'Affordable Housing' has already won and been redistributed
        # we're now redistributing 'Internal organizing'
        # last of that choice's voters already chose 'Affordable Housing'
        # we should go down the user's list of priorities until we find one that hasn't won yet
        # but there isn't one
        e.redistribute_votes(redistribute_from='Internal organizing')
        self.assertEqual(e.redistributed_votes, [
            ['Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None],

            ['Money out of Politics', 'Affordable Housing', 'Good Jobs', 'Immigration',
             'Voting Reform - including Ranked Choice Voting & HR1', 'Indigenous People/Nations',
             None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None]
        ])

    def test_next_ballot__knockout(self):
        self.assertFalse("write this")

    def test_next_ballot__redistribute(self):
        self.assertFalse("write this")

    def test_report(self):
        self.assertFalse("write this")
