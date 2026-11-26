import unittest

from prizes_configs import prize_processor


class TestPrizeProcessor(unittest.TestCase):
    def test_complete_prize(self):
        prize = {
            'prizeAmount': 10000000,
            'prizeAmountAdjusted': 15547541,
            'awardYear': '2001',
            'category': {'en': 'Economic Sciences', 'se': 'Ekonomi'},
            'prizeStatus': 'received',
            'motivation': {'en': 'for their analyses of markets'},
            'sortOrder': '2',
        }
        self.assertEqual(prize_processor()([prize]), [{
            'prize_amount': 10000000,
            'prize_amount_adjusted': 15547541,
            'award_year': 2001,
            'category_en': 'Economic Sciences',
            'prize_status': 'received',
            'motivation': 'for their analyses of markets',
        }])

    def test_missing_fields(self):
        self.assertEqual(prize_processor()([{}]), [{
            'prize_amount': None,
            'prize_amount_adjusted': None,
            'award_year': None,
            'category_en': None,
            'prize_status': None,
            'motivation': None,
        }])

    def test_missing_list(self):
        self.assertEqual(prize_processor()(None), [])
        self.assertEqual(prize_processor()([]), [])

    def test_multiple_prizes_preserve_order(self):
        prizes = [
            {'awardYear': '1911', 'category': {'en': 'Chemistry'}},
            {'awardYear': '1903', 'category': {'en': 'Physics'}},
        ]
        result = prize_processor()(prizes)
        self.assertEqual([prize['award_year'] for prize in result],
                         [1911, 1903])
        self.assertEqual([prize['category_en'] for prize in result],
                         ['Chemistry', 'Physics'])

    def test_integer_year_and_zero_amount(self):
        result = prize_processor()([{'awardYear': 2001, 'prizeAmount': 0}])
        self.assertEqual(result[0]['award_year'], 2001)
        self.assertEqual(result[0]['prize_amount'], 0)


if __name__ == '__main__':
    unittest.main()
