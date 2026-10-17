if __name__ == '__main__':
    days = [
        {'day': 'пн', 'orders': 20, 'revenue': 40_000, 'returns': 2},
        {'day': 'вт', 'orders': 16, 'revenue': 19_200, 'returns': 4},
        {'day': 'ср', 'orders': 25, 'revenue': 55_000, 'returns': 1},
        {'day': 'чт', 'orders': 10, 'revenue': 12_000, 'returns': 3},
        {'day': 'пт', 'orders': 30, 'revenue': 48_000, 'returns': 3},
    ]

    total_revenue = 0
    best_day = days[0]
    bad_days = []

    for day in days:
        total_revenue += day['revenue']
        if day['revenue'] > best_day['revenue']:
            best_day = day
        if day['returns'] / day['orders'] > 0.2:
            bad_days.append(day['day'])

    print('Выручка за неделю:', total_revenue)
    print('Больше всего выручки:', best_day['day'])

    print('Средняя выручка на заказ:')
    for day in days:
        avg = day['revenue'] / day['orders']
        print(day['day'], avg)

    print('Возвратов больше 20%:', bad_days)
