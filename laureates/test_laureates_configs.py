import unittest

from laureates_configs import (
    org_processor,
    person_processor,
    process_orgs,
    process_persons,
    process_year,
)


class TestProcessYear(unittest.TestCase):
    def test_known_years(self):
        for value, expected in (
            ('1943-11-07', 1943),
            ('2001', 2001),
            ('1852-00-00', 1852),
        ):
            with self.subTest(value=value):
                self.assertEqual(process_year(value), expected)

    def test_missing_or_unknown_years(self):
        for value in (None, '', '0000', '0000-00-00', 'unknown', '----'):
            with self.subTest(value=value):
                self.assertIsNone(process_year(value))


class TestLaureateProcessors(unittest.TestCase):
    def test_complete_person(self):
        person = {
            'id': '745',
            'knownName': {'en': 'A. Michael Spence'},
            'gender': 'male',
            'birth': {
                'date': '1943-11-07',
                'place': {
                    'country': {'en': 'USA'},
                    'countryNow': {'en': 'USA'},
                },
            },
            'nobelPrizes': [{
                'prizeAmount': 10000000,
                'prizeAmountAdjusted': 15547541,
                'awardYear': '2001',
                'category': {'en': 'Economic Sciences'},
                'prizeStatus': 'received',
                'motivation': {'en': 'for their analyses of markets'},
            }],
        }
        expected = {
            'id': '745',
            'name': 'A. Michael Spence',
            'gender': 'male',
            'birth_year': 1943,
            'country_birth': 'USA',
            'country_now': 'USA',
            'prizes_relevant': [{
                'prize_amount': 10000000,
                'prize_amount_adjusted': 15547541,
                'award_year': 2001,
                'category_en': 'Economic Sciences',
                'prize_status': 'received',
                'motivation': 'for their analyses of markets',
            }],
        }
        self.assertEqual(person_processor()(person), expected)
        self.assertEqual(process_persons(person), expected)

    def test_complete_organization(self):
        organization = {
            'id': '999',
            'orgName': {'en': 'Example organization'},
            'founded': {
                'date': '1900-01-01',
                'place': {
                    'country': {'en': 'Historical country'},
                    'countryNow': {'en': 'Modern country'},
                },
            },
            'nobelPrizes': [{
                'prizeAmount': 1000000,
                'prizeAmountAdjusted': 2000000,
                'awardYear': '1950',
                'category': {'en': 'Peace'},
                'prizeStatus': 'received',
                'motivation': {'en': 'for humanitarian work'},
            }],
        }
        expected = {
            'id': '999',
            'name': 'Example organization',
            'founded_year': 1900,
            'country_founded': 'Historical country',
            'country_now': 'Modern country',
            'prizes_relevant': [{
                'prize_amount': 1000000,
                'prize_amount_adjusted': 2000000,
                'award_year': 1950,
                'category_en': 'Peace',
                'prize_status': 'received',
                'motivation': 'for humanitarian work',
            }],
        }
        self.assertEqual(org_processor()(organization), expected)
        self.assertEqual(process_orgs(organization), expected)

    def test_missing_person_fields(self):
        self.assertEqual(process_persons({}), {
            'id': None,
            'name': None,
            'gender': None,
            'birth_year': None,
            'country_birth': None,
            'country_now': None,
            'prizes_relevant': [],
        })

    def test_missing_organization_fields(self):
        self.assertEqual(process_orgs({}), {
            'id': None,
            'name': None,
            'founded_year': None,
            'country_founded': None,
            'country_now': None,
            'prizes_relevant': [],
        })

    def test_none_nested_fields(self):
        result = process_persons({'birth': None, 'nobelPrizes': None})
        self.assertIsNone(result['birth_year'])
        self.assertIsNone(result['country_now'])
        self.assertEqual(result['prizes_relevant'], [])

    def test_person_with_multiple_prizes(self):
        person = {
            'id': '6',
            'knownName': {'en': 'Marie Curie'},
            'nobelPrizes': [
                {'awardYear': '1903', 'category': {'en': 'Physics'}},
                {'awardYear': '1911', 'category': {'en': 'Chemistry'}},
            ],
        }
        result = process_persons(person)
        self.assertEqual(result['id'], '6')
        self.assertEqual(len(result['prizes_relevant']), 2)
        self.assertEqual(result['prizes_relevant'][1]['award_year'], 1911)
        self.assertEqual(
            result['prizes_relevant'][1]['category_en'], 'Chemistry'
        )

    def test_organization_with_multiple_prizes(self):
        organization = {
            'orgName': {'en': 'Example organization'},
            'nobelPrizes': [
                {'awardYear': '1917'},
                {'awardYear': '1944'},
                {'awardYear': '1963'},
            ],
        }
        result = process_orgs(organization)
        self.assertEqual(
            [prize['award_year'] for prize in result['prizes_relevant']],
            [1917, 1944, 1963],
        )


if __name__ == '__main__':
    unittest.main()
