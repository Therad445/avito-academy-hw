def filter_data(data, condition):
    """отбор записей по условию"""
    return [record for record in data if condition(record)]


def group_by_attributes(data, attributes):
    """группировка по полям"""
    attributes = tuple(attributes)
    groups = {}
    for record in data:
        key = tuple(record.get(attribute) for attribute in attributes)
        groups.setdefault(key, []).append(record)
    return groups


def aggregate_data(data, aggregations):
    """расчет агрегаций"""
    return {name: function(data) for name, function in aggregations.items()}


def is_missing(value):
    """проверка на None и пустые значения"""
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def count_missing(data, attributes=None):
    """число пропусков по полям"""
    if attributes is None:
        attributes = sorted({name for record in data for name in record})
    return {
        name: sum(is_missing(record.get(name)) for record in data)
        for name in attributes
    }
