"""Скрипт для заполнения данными таблиц в БД Postgres."""
import os
import psycopg2
from dotenv import load_dotenv
from hh_api import HeadHunterAPI
from config import company_ids

# Загрузка переменных окружения из файла .env
load_dotenv()

# Извлечение настроек в переменные
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')


def create_database(database_name: str) -> None:
    """Создание базы данных"""

    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            database='postgres',  # БД, к которой можно подключиться до создания новой
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )

        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
            cursor.execute(f"CREATE DATABASE {database_name}")

        print(f"База данных '{database_name}' успешно создана.")

    except Exception as e:
        print(f'Ошибка: {e}')
    finally:
        if conn:
            conn.close()


def create_table() -> None:
    """Создание таблицы для сохранения данных о вакансиях"""

    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
            )

        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS hh_vacancies")
            cursor.execute("""
                CREATE TABLE hh_vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255) NOT NULL,
                company_name VARCHAR(255) NOT NULL,
                min_salary INT,
                max_salary INT,
                salary_currency VARCHAR(20),
                url VARCHAR(255) NOT NULL
                )
                """)

            print('Таблица hh_vacancies успешно создана.')
    except Exception as e:
        print(f'Ошибка: {e}')
    finally:
        if conn:
            conn.close()


def save_data_to_database() -> None:
    """Сохранение данных о вакансиях в таблицу."""

    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )

        with conn.cursor() as cursor:
            data = HeadHunterAPI()
            vacancies = data.get_vacancies(company_ids)

            for item in vacancies:
                min_salary = item['min_salary'] or 0
                max_salary = item['max_salary'] or 0
                salary_currency = item['salary_currency'] or 'null'

                cursor.execute(
                    """
                    INSERT INTO hh_vacancies (
                    vacancy_name, company_name, min_salary, max_salary, salary_currency, url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (item['name'], item['employer'], min_salary, max_salary, salary_currency, item['url']))

            conn.commit()
    except Exception as e:
        print(f'Ошибка при выполнении запроса: {e}')
    finally:
        if conn:
            conn.close()
