import requests
from abc import ABC, abstractmethod

# Константы
PAGES = 0
PER_PAGE = 30


class APIManager(ABC):
    """Абстрактный класс"""

    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def get_vacancies(self, ids) -> list:
        """Получение вакансий по id компании"""


class HeadHunterAPI(APIManager):
    """Класс для парсинга вакансий с сайта headhunter"""

    def __init__(self, base_url='https://api.hh.ru/'):
        super().__init__(base_url)

    def get_vacancies(self, company_ids: dict) -> list:

        all_vacancies = []  # Пустой список для хранения всей информации о вакансиях
        vacancies_data = []  # Пустой список для хранения информации о вакансиях, необходимой для внесения в базу данных

        # Цикл для обхода компаний и получения их вакансий
        for company_name, company_id in company_ids.items():
            url = f'{self.base_url}vacancies?employer_id={company_id}'
            params = {'pages': PAGES, 'per_page': PER_PAGE}

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                vacancies = response.json().get('items', [])

                all_vacancies.extend(vacancies)

                for vacancy in vacancies:
                    vac = self.parse_vacancy(vacancy)
                    vacancies_data.append(vac)

            except requests.exceptions.RequestException as e:
                print(f'Ошибка при запросе для {company_name}: {str(e)}')

        return vacancies_data

    @staticmethod
    def parse_vacancy(vacancy) -> dict:

        # Получение данных о зарплате
        salary_data = vacancy.get('salary', {})
        if salary_data:
            salary_from = salary_data.get('from') if salary_data.get(
                'from') is not None else None
            salary_to = salary_data.get('to') if salary_data.get(
                'to') is not None else None
            salary_currency = vacancy['salary']['currency']

        else:
            salary_from = None
            salary_to = None
            salary_currency = None

        # Создание словаря с информацией о вакансиях и компаниях
        vac = {'name': vacancy['name'],
               'employer': vacancy['employer']['name'],
               'min_salary': salary_from,
               'max_salary': salary_to,
               'salary_currency': salary_currency,
               'url': vacancy['apply_alternate_url'],
               'company_url': vacancy['employer']['alternate_url'],
               'company_id': vacancy['employer']['id']
               }
        return vac
