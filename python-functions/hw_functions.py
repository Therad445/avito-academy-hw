import csv
from pathlib import Path


def read_file(filename: Path) -> list[dict[str, str]]:
    """Читает информацию о сотрудниках из CSV."""
    with open(filename, encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file, delimiter=';'))


def report_1(data: list[dict[str, str]]) -> None:
    """Выводит департаменты и команды в каждом из них."""
    departments = {}
    for person in data:
        dep = person['Департамент']
        team = person['Отдел']
        if dep not in departments:
            departments[dep] = []
        if team not in departments[dep]:
            departments[dep].append(team)

    for dep, teams in departments.items():
        print(dep)
        for team in teams:
            print(' -', team)


def get_stats(data: list[dict[str, str]]) -> dict:
    """Считает количество сотрудников и зарплаты по департаментам."""
    salaries = {}
    for person in data:
        dep = person['Департамент']
        salary = int(person['Оклад'])
        if dep not in salaries:
            salaries[dep] = []
        salaries[dep].append(salary)

    stats = {}
    for dep, money in salaries.items():
        stats[dep] = [
            len(money), min(money), max(money),
            round(sum(money) / len(money), 2)
        ]
    return stats


def report_2(data: list[dict[str, str]]) -> None:
    """Печатает сводную статистику по департаментам."""
    stats = get_stats(data)
    for dep, nums in stats.items():
        print(dep)
        print('Людей:', nums[0])
        print('Мин зарплата:', nums[1])
        print('Макс зарплата:', nums[2])
        print('Средняя:', nums[3])
        print()


def report_3(data: list[dict[str, str]], filename: Path) -> None:
    """Записывает сводную статистику в отдельный CSV-файл."""
    stats = get_stats(data)
    with open(filename, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'Департамент', 'Кол-во сотрудников',
            'Минимальный оклад', 'Максимальный оклад', 'Средний оклад'
        ])
        for dep, nums in stats.items():
            writer.writerow([dep] + nums)
    print('Сохранил в', filename.name)


def main() -> None:
    """Показывает меню и запускает выбранный отчёт."""
    print('1 - Показать департаменты и команды')
    print('2 - Отчёт по зарплатам')
    print('3 - Сохранить отчёт в CSV')
    choice = input('Выберите пункт: ').strip()

    if choice not in ('1', '2', '3'):
        print('Такого варианта нет')
        return

    folder = Path(__file__).resolve().parent
    data = read_file(folder / 'Corp_Summary.csv')
    if choice == '1':
        report_1(data)
    elif choice == '2':
        report_2(data)
    else:
        report_3(data, folder / 'department_summary.csv')


if __name__ == '__main__':
    main()
