if __name__ == '__main__':
    moscow = {201, 202, 203, 204}
    kazan = {203, 204, 205, 206}

    both = moscow & kazan
    only_moscow = moscow - kazan
    only_kazan = kazan - moscow
    all_items = moscow | kazan

    print('В обоих городах:', sorted(both))
    print('Только Москва:', sorted(only_moscow))
    print('Только Казань:', sorted(only_kazan))
    print('Всего разных товаров:', len(all_items))
