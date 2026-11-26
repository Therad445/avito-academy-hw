"""тесты агрегаций и сортировки"""

import unittest

from aggregations import (
    count_records,
    max_value,
    mean_value,
    median_value,
    min_value,
    top_n,
)


class AggregationsTests(unittest.TestCase):
    def test_count_records(self):
        self.assertEqual(count_records([]), 0)
        self.assertEqual(count_records([{}, {'age': None}]), 2)

    def test_numeric_aggregations_ignore_none_and_missing_keys(self):
        data = [{'age': 0}, {'age': 10}, {}, {'age': None}, {'age': 20}]
        self.assertEqual(mean_value(data, 'age'), 10)
        self.assertEqual(median_value(data, 'age'), 10)
        self.assertEqual(min_value(data, 'age'), 0)
        self.assertEqual(max_value(data, 'age'), 20)
        self.assertEqual(median_value([{'age': 2}, {'age': 4}], 'age'), 3)

    def test_empty_aggregations_return_none(self):
        for function in (mean_value, median_value, min_value, max_value):
            for data in ([], [{}, {'age': None}]):
                with self.subTest(function=function.__name__, data=data):
                    self.assertIsNone(function(data, 'age'))

    def test_values_are_not_parsed_or_silently_discarded(self):
        with self.assertRaises(TypeError):
            mean_value([{'age': '10'}], 'age')
        with self.assertRaises(TypeError):
            mean_value([{'age': ''}], 'age')
        self.assertEqual(min_value([{'value': ''}], 'value'), '')
        self.assertEqual(min_value([{'value': False}], 'value'), False)

    def test_top_n_is_stable_and_preserves_original_data(self):
        data = [
            {'id': 'a', 'age': 20},
            {'id': 'b', 'age': 30},
            {'id': 'c', 'age': 30},
            {'id': 'd', 'age': None},
            {'id': 'e'},
        ]
        result = top_n(data, 'age', 2)
        self.assertEqual([record['id'] for record in result], ['b', 'c'])
        self.assertIs(result[0], data[1])
        self.assertEqual([record['id'] for record in data], list('abcde'))
        self.assertEqual(top_n(data, 'age', 10, reverse=False), data[:3])

    def test_top_n_handles_empty_and_zero_limits(self):
        self.assertEqual(top_n([], 'age'), [])
        self.assertEqual(top_n([{}, {'age': None}], 'age'), [])
        self.assertEqual(top_n([{'age': 20}], 'age', 0), [])
        data = [{'age': age} for age in range(7)]
        self.assertEqual(len(top_n(data, 'age')), 5)

    def test_top_n_rejects_invalid_limits(self):
        for value in (-1, 1.5, '2', None, True, False):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    top_n([], 'age', value)
