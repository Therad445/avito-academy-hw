import unittest

from json_dict_processing import (
    create_processor,
    extract_nested_value,
    process_dictionary_with_config,
    process_list_of_dicts_with_config,
)


class TestExtractNestedValue(unittest.TestCase):
    def test_nested_dictionary(self):
        data = {'birth': {'place': {'country': 'Denmark'}}}
        self.assertEqual(
            extract_nested_value(data, ['birth', 'place', 'country']),
            'Denmark',
        )

    def test_empty_path_returns_original_object(self):
        data = {'name': 'Alice'}
        self.assertIs(extract_nested_value(data, []), data)

    def test_missing_keys_and_invalid_containers(self):
        for data in ({}, {'birth': None}, {'birth': 1943}, None):
            with self.subTest(data=data):
                self.assertIsNone(
                    extract_nested_value(data, ['birth', 'date'])
                )

    def test_list_index_in_path(self):
        data = {'prizes': [{'year': 1903}, {'year': 1911}]}
        self.assertEqual(
            extract_nested_value(data, ['prizes', 1, 'year']),
            1911,
        )

    def test_unavailable_list_index(self):
        for key in (2, -3, '0'):
            with self.subTest(key=key):
                self.assertIsNone(extract_nested_value([1, 2], [key]))

    def test_false_and_zero_are_preserved(self):
        self.assertEqual(extract_nested_value({'value': 0}, ['value']), 0)
        self.assertIs(
            extract_nested_value({'value': False}, ['value']), False
        )


class TestDictionaryProcessing(unittest.TestCase):
    def test_raw_transformed_and_missing_fields(self):
        data = {'name': {'en': 'Alice'}, 'year': '2001', 'extra': True}
        config = {
            'name': ['name', 'en'],
            'year': (['year'], int),
            'country': ['country', 'en'],
        }
        self.assertEqual(
            process_dictionary_with_config(data, config),
            {'name': 'Alice', 'year': 2001, 'country': None},
        )
        self.assertEqual(data['year'], '2001')
        self.assertIn('extra', data)

    def test_processor_receives_none(self):
        received = []

        def replace_missing(value):
            received.append(value)
            return [] if value is None else value

        config = {'prizes': (['missing'], replace_missing)}
        self.assertEqual(
            process_dictionary_with_config({}, config), {'prizes': []}
        )
        self.assertEqual(received, [None])

    def test_list_processing(self):
        data = [{'year': '1903'}, {'year': '1911'}]
        config = {'award_year': (['year'], int)}
        self.assertEqual(
            process_list_of_dicts_with_config(data, config),
            [{'award_year': 1903}, {'award_year': 1911}],
        )

    def test_empty_or_missing_list(self):
        for data in (None, []):
            with self.subTest(data=data):
                self.assertEqual(
                    process_list_of_dicts_with_config(data, {}), []
                )

    def test_dictionary_processor_factory(self):
        processor = create_processor({'name': ['name', 'en']})
        self.assertEqual(
            processor({'name': {'en': 'Alice'}}), {'name': 'Alice'}
        )
        self.assertEqual(processor({}), {'name': None})

    def test_list_processor_factory(self):
        processor = create_processor({'id': ['id']}, list_processor=True)
        self.assertEqual(processor([{'id': '1'}]), [{'id': '1'}])
        self.assertEqual(processor(None), [])


if __name__ == '__main__':
    unittest.main()
