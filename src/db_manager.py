import os

import psycopg2
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()


class DBManager:
    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        """Открывает соединение с БД"""

        db_params = {
            'host': os.getenv('DATABASE_HOST'),
            'database': os.getenv('DATABASE_NAME'),
            'user': os.getenv('DATABASE_USER'),
            'password': os.getenv('DATABASE_PASSWORD')
        }

        self.conn = psycopg2.connect(**db_params)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрывает соединение с БД"""

        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        """Отправляет запрос к БД, возвращает данные и обрабатывает возможные ошибки"""

        try:
            self.cur.execute(query, params)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f'Ошибка при выполнении запроса: {e}')
            return []

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""

        query = """
             SELECT company_name, COUNT(vacancy_name)
             FROM hh_vacancies
             JOIN employers USING (company_id)
             GROUP BY company_name
             ORDER BY company_name;
             """

        return self.execute_query(query)

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """

        query = """
        SELECT vacancy_name, company_name,  min_salary, max_salary, salary_currency, vac.url 
        FROM hh_vacancies AS vac
        JOIN employers USING (company_id);
        """

        return self.execute_query(query)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям в компании."""

        query = """
            SELECT company_name,
            ROUND(AVG(
                     CASE
                        WHEN min_salary = 0 AND max_salary = 0 THEN NULL
                        WHEN min_salary = 0 THEN max_salary
                        WHEN max_salary = 0 THEN min_salary
                        ELSE (min_salary + max_salary) / 2
                    END
                )) AS average_salary, salary_currency
            FROM hh_vacancies
            JOIN employers USING (company_id)
            WHERE NOT (min_salary = 0 AND max_salary = 0)
            GROUP BY company_name, salary_currency
            ORDER BY average_salary DESC;
            """

        return self.execute_query(query)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        query = """
            SELECT vacancy_name, company_name, min_salary, salary_currency, vac.url
            FROM hh_vacancies AS vac
            JOIN employers USING (company_id)
            WHERE min_salary > (SELECT ROUND(AVG(
                    CASE
                        WHEN min_salary = 0 AND max_salary = 0 THEN NULL
                        WHEN min_salary = 0 THEN max_salary
                        WHEN max_salary = 0 THEN min_salary
                        ELSE (min_salary + max_salary) / 2
                    END
                )) FROM hh_vacancies)
            ORDER BY min_salary DESC;
            """

        return self.execute_query(query)

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные ключевые слова."""

        query = """
            SELECT vacancy_name, company_name,  min_salary, max_salary, salary_currency, vac.url
            FROM hh_vacancies AS vac
            JOIN employers USING (company_id)
            WHERE vacancy_name iLIKE %s;
            """

        params = ('%' + keyword + '%',)  # Параметр для поиска
        return self.execute_query(query, params)
