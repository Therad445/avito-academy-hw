if __name__ == '__main__':
    reviews = [
        {'id': 1, 'product': 'Чехол', 'stars': 5},
        {'id': 1, 'product': 'Чехол', 'stars': 3},
        {'id': 1, 'product': 'Чехол', 'stars': 4},
        {'id': 2, 'product': 'Наушники', 'stars': 2},
        {'id': 2, 'product': 'наушники', 'stars': 2},
        {'id': 2, 'product': 'НАУШНИКИ', 'stars': 5},
        {'id': 3, 'product': 'Планшет', 'stars': 5},
        {'id': 4, 'product': 'Колонка', 'stars': 4},
        {'id': 4, 'product': 'Колонка', 'stars': 4},
        {'id': 5, 'product': 'Кабель', 'stars': 1},
    ]

    scores = {}
    low_count = 0

    for review in reviews:
        name = review['product'].lower()
        if name not in scores:
            scores[name] = [0, 0]
        scores[name][0] += review['stars']
        scores[name][1] += 1

        if review['stars'] <= 2:
            low_count += 1

    avg_stars = {}
    worst = None
    for name in scores:
        total, count = scores[name]
        avg_stars[name] = total / count
        if count >= 2:
            if worst is None or avg_stars[name] < avg_stars[worst]:
                worst = name

    print('Средние оценки:', avg_stars)
    print('Худший товар с 2+ отзывами:', worst, avg_stars[worst])
    print('Отзывов на 1 или 2 звезды:', low_count)
    print('Их доля:', low_count / len(reviews) * 100, '%')
