if __name__ == '__main__':
    orders = [
        {'id': 1, 'buyer': 'anya', 'status': 'delivered', 'amount': 900},
        {'id': 2, 'buyer': 'boris', 'status': 'returned', 'amount': 4_500},
        {'id': 3, 'buyer': 'anya', 'status': 'delivered', 'amount': 1_500},
        {'id': 4, 'buyer': 'vera', 'status': 'delivered', 'amount': 3_200},
        {'id': 5, 'buyer': 'boris', 'status': 'delivered', 'amount': 700},
        {'id': 6, 'buyer': 'gleb', 'status': 'returned', 'amount': 2_100},
    ]

    returned_sum = 0
    returned_buyers = set()
    delivered_count = 0
    delivered_sum = 0

    for order in orders:
        if order['status'] == 'returned':
            returned_sum += order['amount']
            returned_buyers.add(order['buyer'])
        elif order['status'] == 'delivered':
            delivered_count += 1
            delivered_sum += order['amount']

    print('Сумма возвратов:', returned_sum)
    print('Кто возвращал:', sorted(returned_buyers))
    print('Доставлено заказов:', delivered_count)
    print('Средний чек:', delivered_sum / delivered_count)
