import csv
import sys


def read_file(filename):
    with open(filename, encoding='utf-8-sig', newline='') as f:
        data = csv.DictReader(f, delimiter=';')
        return list(data)


def report_1(data):
    deps = {}
    for person in data:
        dep = person['Департамент']
        team = person['Отдел']
        if dep not in deps:
            deps[dep] = []
        if team not in deps[dep]:
            deps[dep].append(team)

    for dep in deps:
        print(dep)
        for team in deps[dep]:
            print(' -', team)


def get_stats(data):
    deps = {}
    for person in data:
        dep = person['Департамент']
        salary = int(person['Оклад'])
        if dep not in deps:
            deps[dep] = []
        deps[dep].append(salary)

    result = {}
    for dep in deps:
        money = deps[dep]
        result[dep] = [len(money), min(money), max(money),
                       round(sum(money) / len(money), 2)]
    return result


def report_2(data):
    stats = get_stats(data)
    for dep in stats:
        nums = stats[dep]
        print(dep)
        print('Людей:', nums[0])
        print('Мин зарплата:', nums[1])
        print('Макс зарплата:', nums[2])
        print('Средняя:', nums[3])
        print()


def report_3(data, filename='department_summary.csv'):
    stats = get_stats(data)
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Департамент', 'Кол-во сотрудников',
                         'Минимальный оклад', 'Максимальный оклад',
                         'Средний оклад'])
        for dep in stats:
            writer.writerow([dep] + stats[dep])
    print('Сохранил в', filename)


def main(variant):
    if variant not in (1, 2, 3):
        print('Такого варианта нет')
        return

    data = read_file('Corp_Summary.csv')
    if variant == 1:
        report_1(data)
    elif variant == 2:
        report_2(data)
    elif variant == 3:
        report_3(data)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Укажи номер отчета: 1, 2 или 3')
    else:
        try:
            main(int(sys.argv[1]))
        except ValueError:
            print('Нужно ввести число')
