from src.postgres_database import create_database, create_table, save_data_to_database
from db_manager import DBManager


def main():
    create_database('headhunter')  # Вызов функции для создания Базы Данных
    create_table()  # Вызов функции для создания таблицы
    save_data_to_database()  # Сохранение данных о вакансиях в таблицу

    with DBManager() as db:
        while True:
            print()
            user_command = input('Выберите команду для запроса: \n'
                                 '1 - Вывести список всех компаний и количество вакансий у каждой компании;\n'
                                 '2 - Вывести список всех вакансий;\n'
                                 '3 - Вывести среднюю зарплату по вакансиям для каждой компании;\n'
                                 '4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям;\n'
                                 '5 - Вывести список всех вакансий по ключевому слову в названии названии вакансий;\n'
                                 '0 - Выход.\n'
                                 )

            if user_command == '0':
                print('Работа программы завершена.')
                break

            elif user_command == '1':
                data = db.get_companies_and_vacancies_count()
                for i in data:
                    company, count = i
                    print(f'{company}: {count} вакансий')

            elif user_command == '2':
                data = db.get_all_vacancies()
                for i in data:
                    salary = 'не указана' if i[3] == 0 and i[4] == 0 else (
                        f'{i[4]} {i[-2]}' if i[3] == 0 else f'{i[3]} {i[-2]}')

                    print(f'Вакансия "{i[1]}", компания {i[2]},\n'
                          f'зарплата - {salary}, ссылка - {i[-1]}')
                    print()

            elif user_command == '3':
                data = db.get_avg_salary()
                for i in data:
                    company, avg_salary, currency = i
                    print(f'Средняя зарплата по вакансиям компании {company} - {avg_salary} {currency}')

            elif user_command == '4':
                data = db.get_vacancies_with_higher_salary()
                for i in data:
                    print(f'Вакансия "{i[0]}", компания {i[1]},\n'
                          f'зарплата {i[2]} {i[3]}, ссылка - {i[4]}')
                    print()

            elif user_command.lower() == '5':
                keyword = input('Введите ключевое слово для поиска вакансий: ')
                data = db.get_vacancies_with_keyword(keyword)
                for i in data:
                    salary = 'не указана' if i[3] == 0 and i[4] == 0 else (
                        f'{i[4]} {i[-2]}' if i[3] == 0 else f'{i[3]} {i[-2]}')

                    print(f'Вакансия "{i[1]}", компания {i[2]},\n'
                          f'зарплата - {salary}, ссылка - {i[-1]}')
                    print()

            else:
                print('Неверная команда. Попробуйте ещё раз.')


if __name__ == '__main__':
    main()
