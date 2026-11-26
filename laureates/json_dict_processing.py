def extract_nested_value(obj, keys):
    """значение по пути, иначе None"""
    value = obj
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        elif isinstance(value, list) and isinstance(key, int):
            try:
                value = value[key]
            except IndexError:
                return None
        else:
            return None
    return value


def process_dictionary_with_config(dictionary, config):
    """обработка полей по конфигу"""
    result = {}
    for attribute, rule in config.items():
        if isinstance(rule, tuple):
            keys, processor = rule
            result[attribute] = processor(
                extract_nested_value(dictionary, keys)
            )
        else:
            result[attribute] = extract_nested_value(dictionary, rule)
    return result


def process_list_of_dicts_with_config(list_of_dicts, config):
    """обработка списка словарей, для None результат []"""
    return [
        process_dictionary_with_config(dictionary, config)
        for dictionary in (list_of_dicts or [])
    ]


def create_processor(config, list_processor=False):
    """процессор с готовым конфигом"""
    if list_processor:
        processor = process_list_of_dicts_with_config
    else:
        processor = process_dictionary_with_config

    def process(data):
        return processor(data, config)

    return process
