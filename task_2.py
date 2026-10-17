if __name__ == '__main__':
    queries = [
        'чехол',
        'iphone',
        'чехол',
        'наушники',
        'iphone',
        'iphone',
        'кабель',
        'чехол',
        'iphone',
    ]

    counts = {}
    for query in queries:
        counts[query] = counts.get(query, 0) + 1

    top_query = max(counts, key=counts.get)
    one_time = []
    for query in counts:
        if counts[query] == 1:
            one_time.append(query)

    print('Всего запросов:', len(queries))
    print('Сколько раз искали:', counts)
    print('Самый частый:', top_query)
    print('Его доля:', round(counts[top_query] / len(queries) * 100, 2), '%')
    print('По одному разу:', one_time)
