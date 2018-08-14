import unittest
from unittest.mock import patch
from election.Election import Election


class ElectionTestCase(unittest.TestCase):
    def test_preen_voter_ids(self):
        e = Election()
        e.data = [
            {
                'Email Address': 'Bobbie.Gentry@gmail.com',
                '[Black Sabbath]': 'First Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'Third Preference',
                '\ufeffTimestamp': '8/3/2018 12:10:04'
            },

            {
                'Email Address': 'tom.jones@GMAIL.com',
                '[Black Sabbath]': 'Second Preference',
                '[Napalm Death]': 'First Preference',
                '[Cradle of Filth]': 'Third Preference',
                '\ufeffTimestamp': '8/4/2018 13:10:04'
            },

            {
                'Email Address': 5,
                '[Black Sabbath]': '',
                '[Napalm Death]': 'First Preference',
                '[Cradle of Filth]': '',
                '\ufeffTimestamp': '8/4/2018 13:10:04'
            }
        ]

        e.data = e.preen_voter_ids(e.data, e.voter_id_col)
        self.assertEqual(
            [
                {
                    'Email Address': 'bobbie.gentry@gmail.com',
                    '[Black Sabbath]': 'First Preference',
                    '[Napalm Death]': 'Second Preference',
                    '[Cradle of Filth]': 'Third Preference',
                    '\ufeffTimestamp': '8/3/2018 12:10:04'
                },

                {
                    'Email Address': 'tom.jones@gmail.com',
                    '[Black Sabbath]': 'Second Preference',
                    '[Napalm Death]': 'First Preference',
                    '[Cradle of Filth]': 'Third Preference',
                    '\ufeffTimestamp': '8/4/2018 13:10:04'
                },

                {
                    'Email Address': '5',
                    '[Black Sabbath]': '',
                    '[Napalm Death]': 'First Preference',
                    '[Cradle of Filth]': '',
                    '\ufeffTimestamp': '8/4/2018 13:10:04'
                }
            ],
            e.data
        )

    def test_cleanup_timestamp_col(self):
        e = Election()
        e.data = [
            {
                'Email Address': 'bobbie.gentry@gmail.com',
                '[Black Sabbath]': 'First Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'Third Preference',
                '\ufeffTimestamp': '8/3/2018 12:10:04'
            },

            {
                'Email Address': 'bobbie.gentry@gmail.com',
                '[Black Sabbath]': 'Third Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'First Preference',
                '\ufeffTimestamp': '8/4/2018 11:10:04'
            },

            {
                'Email Address': 'tom.jones@gmail.com',
                '[Black Sabbath]': 'First Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'Third Preference',
                '\ufeffTimestamp': '8/4/2018 12:10:04'
            },

            {
                'Email Address': 'tom.jones@gmail.com',
                '[Black Sabbath]': 'Second Preference',
                '[Napalm Death]': 'First Preference',
                '[Cradle of Filth]': 'Third Preference',
                '\ufeffTimestamp': '8/4/2018 13:10:04'
            },

            {
                'Email Address': 'glen.campbell@gmail.com',
                '[Black Sabbath]': '',
                '[Napalm Death]': 'First Preference',
                '[Cradle of Filth]': '',
                '\ufeffTimestamp': '8/4/2018 13:10:04'
            }
        ]

        e.cleanup_unicode()
        self.maxDiff = None

        self.assertEqual(
            e.data, [
                {
                    'Email Address': 'bobbie.gentry@gmail.com',
                    '[Black Sabbath]': 'First Preference',
                    '[Napalm Death]': 'Second Preference',
                    '[Cradle of Filth]': 'Third Preference',
                    'Timestamp': '8/3/2018 12:10:04'
                },

                {
                    'Email Address': 'bobbie.gentry@gmail.com',
                    '[Black Sabbath]': 'Third Preference',
                    '[Napalm Death]': 'Second Preference',
                    '[Cradle of Filth]': 'First Preference',
                    'Timestamp': '8/4/2018 11:10:04'
                },

                {
                    'Email Address': 'tom.jones@gmail.com',
                    '[Black Sabbath]': 'First Preference',
                    '[Napalm Death]': 'Second Preference',
                    '[Cradle of Filth]': 'Third Preference',
                    'Timestamp': '8/4/2018 12:10:04'
                },

                {
                    'Email Address': 'tom.jones@gmail.com',
                    '[Black Sabbath]': 'Second Preference',
                    '[Napalm Death]': 'First Preference',
                    '[Cradle of Filth]': 'Third Preference',
                    'Timestamp': '8/4/2018 13:10:04'
                },

                {
                    'Email Address': 'glen.campbell@gmail.com',
                    '[Black Sabbath]': '',
                    '[Napalm Death]': 'First Preference',
                    '[Cradle of Filth]': '',
                    'Timestamp': '8/4/2018 13:10:04'
                }
            ]
        )

    def test_dedupe(self):
        e = Election()
        e.data = [
            {
                'Email Address': 'bobbie.gentry@gmail.com',
                '[Black Sabbath]': 'First Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'Third Preference',
                'Timestamp': '8/3/2018 12:10:04'
            },

            {
                'Email Address': 'bobbie.gentry@gmail.com',
                '[Black Sabbath]': 'Third Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'First Preference',
                'Timestamp': '8/4/2018 11:10:04'
            },

            {
                'Email Address': 'tom.jones@gmail.com',
                '[Black Sabbath]': 'First Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'Third Preference',
                'Timestamp': '8/5/2018 12:10:04'
            },

            {
                'Email Address': 'tom.jones@gmail.com',
                '[Black Sabbath]': 'Second Preference',
                '[Napalm Death]': 'First Preference',
                '[Cradle of Filth]': 'Third Preference',
                'Timestamp': '8/5/2018 13:10:04'
            },

            {
                'Email Address': 'glen.campbell@gmail.com',
                '[Black Sabbath]': '',
                '[Napalm Death]': 'First Preference',
                '[Cradle of Filth]': '',
                'Timestamp': '8/4/2018 13:10:04'
            }
        ]

        e.dedupe()
        self.maxDiff = None

        self.assertEqual(
            e.data, [
                {
                    'Email Address': 'bobbie.gentry@gmail.com',
                    '[Black Sabbath]': 'Third Preference',
                    '[Napalm Death]': 'Second Preference',
                    '[Cradle of Filth]': 'First Preference',
                    'Timestamp': '8/4/2018 11:10:04'
                },

                {
                    'Email Address': 'tom.jones@gmail.com',
                    '[Black Sabbath]': 'Second Preference',
                    '[Napalm Death]': 'First Preference',
                    '[Cradle of Filth]': 'Third Preference',
                    'Timestamp': '8/5/2018 13:10:04'
                },

                {
                    'Email Address': 'glen.campbell@gmail.com',
                    '[Black Sabbath]': '',
                    '[Napalm Death]': 'First Preference',
                    '[Cradle of Filth]': '',
                    'Timestamp': '8/4/2018 13:10:04'
                }
            ]
        )

    def test_find_interlopers(self):
        e = Election()
        e.data = [
            {
                'Email Address': 'bobbie.gentry@gmail.com',
                '[Black Sabbath]': 'First Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'Third Preference',
                'Timestamp': '8/3/2018 12:10:04'
            },

            {
                'Email Address': 'bobbie.gentry@gmail.com',
                '[Black Sabbath]': 'Third Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'First Preference',
                'Timestamp': '8/4/2018 11:10:04'
            },

            {
                'Email Address': 'tom.jones@gmail.com',
                '[Black Sabbath]': 'First Preference',
                '[Napalm Death]': 'Second Preference',
                '[Cradle of Filth]': 'Third Preference',
                'Timestamp': '8/5/2018 12:10:04'
            },

            {
                'Email Address': 'tom.jones@gmail.com',
                '[Black Sabbath]': 'Second Preference',
                '[Napalm Death]': 'First Preference',
                '[Cradle of Filth]': 'Third Preference',
                'Timestamp': '8/5/2018 13:10:04'
            },

            {
                'Email Address': 'glen.campbell@gmail.com',
                '[Black Sabbath]': '',
                '[Napalm Death]': 'First Preference',
                '[Cradle of Filth]': '',
                'Timestamp': '8/4/2018 13:10:04'
            }
        ]

        e.registration_data = [
            {
                'email': 'glen.campbell@gmail.com',
                'first_name': 'Glen',
                'last_name': 'Campbell'
            },
            {
                'email': 'bobbie.gentry@gmail.com',
                'first_name': 'Bobbie',
                'last_name': 'Gentry'
            }
        ]

        e.find_interlopers()
        self.assertEqual(
            [
                {
                    'Email Address': 'tom.jones@gmail.com',
                    '[Black Sabbath]': 'First Preference',
                    '[Napalm Death]': 'Second Preference',
                    '[Cradle of Filth]': 'Third Preference',
                    'Timestamp': '8/5/2018 12:10:04'
                },

                {
                    'Email Address': 'tom.jones@gmail.com',
                    '[Black Sabbath]': 'Second Preference',
                    '[Napalm Death]': 'First Preference',
                    '[Cradle of Filth]': 'Third Preference',
                    'Timestamp': '8/5/2018 13:10:04'
                }
            ],
            e.interlopers
        )