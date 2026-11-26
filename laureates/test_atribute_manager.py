"""тесты добавления и удаления полей"""

import unittest

from atribute_manager import add_attribute, remove_attribute


class AttributeManagerTests(unittest.TestCase):
    def test_add_attribute_copies_records_and_preserves_source(self):
        data = [{'year': 1901, 'tags': ['physics']}, {'year': 1902}]
        result = add_attribute(data, 'decade', lambda row: row['year'] // 10)
        self.assertEqual(result[0]['decade'], 190)
        self.assertEqual(result[1]['decade'], 190)
        self.assertNotIn('decade', data[0])
        self.assertNotIn('decade', data[1])
        self.assertIsNot(result, data)
        self.assertIsNot(result[0], data[0])
        self.assertIs(result[0]['tags'], data[0]['tags'])

    def test_processor_receives_original_record_before_replacement(self):
        data = [{'value': 10}]
        seen = []

        def processor(record):
            seen.append(record)
            return record['value'] * 2

        result = add_attribute(data, 'value', processor)
        self.assertIs(seen[0], data[0])
        self.assertEqual(result, [{'value': 20}])
        self.assertEqual(data, [{'value': 10}])

    def test_remove_attribute_copies_and_accepts_missing_fields(self):
        data = [{'year': 1901, 'tags': ['physics']}, {'year': 1902}]
        result = remove_attribute(data, 'year')
        self.assertEqual(result, [{'tags': ['physics']}, {}])
        self.assertEqual(data[0]['year'], 1901)
        self.assertEqual(data[1]['year'], 1902)
        self.assertIsNot(result[0], data[0])
        self.assertIs(result[0]['tags'], data[0]['tags'])
        missing = remove_attribute(data, 'absent')
        self.assertEqual(missing, data)
        self.assertIsNot(missing[1], data[1])

    def test_empty_data_returns_new_empty_lists(self):
        data = []
        added = add_attribute(data, 'unused', lambda record: 1 / 0)
        removed = remove_attribute(data, 'unused')
        self.assertEqual(added, [])
        self.assertEqual(removed, [])
        self.assertIsNot(added, data)
        self.assertIsNot(removed, data)
