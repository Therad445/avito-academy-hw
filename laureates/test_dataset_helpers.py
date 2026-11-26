"""тесты фильтрации, группировки и пропусков"""

import unittest

from dataset_helpers import (
    aggregate_data,
    count_missing,
    filter_data,
    group_by_attributes,
    is_missing,
)


class DatasetHelpersTests(unittest.TestCase):
    def test_filter_preserves_order_and_original_records(self):
        data = [{'year': 1901}, {'year': 1903}, {'year': 1902}]
        result = filter_data(data, lambda record: record['year'] > 1901)
        self.assertEqual(result, [{'year': 1903}, {'year': 1902}])
        self.assertIs(result[0], data[1])
        self.assertEqual(filter_data([], lambda record: True), [])

    def test_group_by_multiple_fields_and_missing_field(self):
        data = [
            {'category': 'physics', 'year': 1901, 'id': 1},
            {'category': 'physics', 'year': 1901, 'id': 2},
            {'category': 'chemistry', 'year': 1901, 'id': 3},
            {'category': 'physics', 'id': 4},
        ]
        result = group_by_attributes(data, ['category', 'year'])
        self.assertEqual(list(result), [
            ('physics', 1901), ('chemistry', 1901), ('physics', None),
        ])
        self.assertEqual(result[('physics', 1901)], data[:2])
        self.assertIs(result[('physics', None)][0], data[3])

    def test_group_empty_data_and_empty_attributes(self):
        self.assertEqual(group_by_attributes([], ['category']), {})
        data = [{'id': 1}, {'id': 2}]
        self.assertEqual(group_by_attributes(data, []), {(): data})

    def test_aggregate_named_functions(self):
        data = [{'year': 1901}, {'year': 1902}]
        result = aggregate_data(data, {
            'count': len,
            'latest': lambda rows: max(row['year'] for row in rows),
        })
        self.assertEqual(result, {'count': 2, 'latest': 1902})
        self.assertEqual(aggregate_data([], {'count': len}), {'count': 0})
        self.assertEqual(aggregate_data(data, {}), {})

    def test_is_missing_recognizes_only_supported_values(self):
        for value in (None, '', ' \t\n', [], {}):
            with self.subTest(value=value):
                self.assertTrue(is_missing(value))
        for value in (0, False, '0', ' text ', [None], {'a': None}, (), set()):
            with self.subTest(value=value):
                self.assertFalse(is_missing(value))

    def test_count_missing_uses_sorted_union_and_keeps_zero_false(self):
        data = [
            {'b': 0, 'a': None, 'c': []},
            {'b': False, 'a': ' ', 'd': {}},
            {'b': '', 'a': 'present', 'c': [1]},
        ]
        result = count_missing(data)
        self.assertEqual(result, {'a': 2, 'b': 1, 'c': 2, 'd': 3})
        self.assertEqual(list(result), ['a', 'b', 'c', 'd'])

    def test_count_missing_selected_fields_and_empty_data(self):
        self.assertEqual(
            count_missing([{'a': 1}, {}], ['missing', 'a']),
            {'missing': 2, 'a': 1},
        )
        self.assertEqual(count_missing([]), {})
        self.assertEqual(count_missing([], ['a']), {'a': 0})
        self.assertEqual(count_missing([{'a': None}], []), {})
