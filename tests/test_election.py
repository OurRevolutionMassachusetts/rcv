import unittest
from unittest.mock import patch
from election.Election import Election


class ElectionTestCase(unittest.TestCase):
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
