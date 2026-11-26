def add_attribute(data, name, processor):
    """добавление поля без изменения исходных записей"""
    result = []
    for record in data:
        updated = record.copy()
        updated[name] = processor(record)
        result.append(updated)
    return result


def remove_attribute(data, name):
    """удаление поля из копий"""
    result = []
    for record in data:
        updated = record.copy()
        updated.pop(name, None)
        result.append(updated)
    return result
