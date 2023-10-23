___
## База данных вакансий с сайта HeadHunter
Цель проекта заключается в создании базы данных для хранения полученных информации о работодателях и их вакансиях.

### Описание файлов

+ main.py содержит функцию main, которая запускает цепочку действий по созданию базы данных PostgresSQL, записи данных в таблицу, а также взаимодействует с пользователем, предлагая командны для получения информации о вакансиях.

+ db_manager.py содержит класс DBManager, который отправляет запросы к базе данных.

+ postgres_database.py содержит функции для создания базы данных headhunter, таблицы hh_vacancies, и заполнения её данными с сайта HeadHunter.

+ hh_api.py содержит класс HeadHunterAPI, который подключается к сайту по api и получает информацию о вакансиях для компаний из списка в файле config.py.

___

###  Установка и использование
Для работы программы необходимо установить зависимости, указанные в файле pyproject.toml

Для работы с базой данных необходимо создать файл .env с параметрами доступа к базе данных PostgresSQL. Пример содержимого файла:
```
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_PORT=1111
POSTGRES_DB=postgres

```