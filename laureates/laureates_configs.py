from json_dict_processing import create_processor
from prizes_configs import prize_processor


def process_year(year_string):
    """год из даты, месяц и день не нужны"""
    if not year_string:
        return None
    try:
        year = int(year_string.split('-')[0])
    except (AttributeError, ValueError):
        return None
    return year if year != 0 else None


CONFIG_PERSON = {
    'id': ['id'],
    'name': ['knownName', 'en'],
    'gender': ['gender'],
    'birth_year': (['birth', 'date'], process_year),
    'country_birth': ['birth', 'place', 'country', 'en'],
    'country_now': ['birth', 'place', 'countryNow', 'en'],
    'prizes_relevant': (['nobelPrizes'], prize_processor()),
}

CONFIG_ORG = {
    'id': ['id'],
    'name': ['orgName', 'en'],
    'founded_year': (['founded', 'date'], process_year),
    'country_founded': ['founded', 'place', 'country', 'en'],
    'country_now': ['founded', 'place', 'countryNow', 'en'],
    'prizes_relevant': (['nobelPrizes'], prize_processor()),
}


def person_processor():
    """процессор для людей"""
    return create_processor(CONFIG_PERSON)


def org_processor():
    """процессор для организаций"""
    return create_processor(CONFIG_ORG)


process_persons = person_processor()
process_orgs = org_processor()
