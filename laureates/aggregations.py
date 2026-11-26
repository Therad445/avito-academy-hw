from statistics import mean, median


def _values(data, attribute):
    """значения поля без None"""
    return [
        record[attribute] for record in data
        if record.get(attribute) is not None
    ]


def count_records(data):
    return len(data)


def mean_value(data, attribute):
    values = _values(data, attribute)
    return mean(values) if values else None


def median_value(data, attribute):
    values = _values(data, attribute)
    return median(values) if values else None


def min_value(data, attribute):
    values = _values(data, attribute)
    return min(values) if values else None


def max_value(data, attribute):
    values = _values(data, attribute)
    return max(values) if values else None


def top_n(data, attribute, n=5, reverse=True):
    """первые n записей после сортировки"""
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError('n должно быть целым неотрицательным числом')
    records = [record for record in data if record.get(attribute) is not None]
    return sorted(
        records, key=lambda record: record[attribute], reverse=reverse
    )[:n]
