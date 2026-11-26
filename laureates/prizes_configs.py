from json_dict_processing import create_processor


CONFIG_PRIZE = {
    'prize_amount': ['prizeAmount'],
    'prize_amount_adjusted': ['prizeAmountAdjusted'],
    'award_year': (
        ['awardYear'],
        lambda value: int(value) if value is not None else None,
    ),
    'category_en': ['category', 'en'],
    'prize_status': ['prizeStatus'],
    'motivation': ['motivation', 'en'],
}


def prize_processor():
    """процессор для списка премий"""
    return create_processor(CONFIG_PRIZE, list_processor=True)
