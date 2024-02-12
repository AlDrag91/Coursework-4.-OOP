import json
from abc import ABC, abstractmethod

import requests


class AbstractJobAPI(ABC):

    @abstractmethod
    def make_request(self):
        pass


class SiteAPIHH(AbstractJobAPI):

    def __init__(self, params):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = params

    def make_request(self) -> list:
        response = requests.get(self.url, self.params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            raise Exception("Ошибка: Запрос не выполнен.")


class Vacancy:
    """Работа с вакансиями."""

    def __init__(self, id_vacancy, title, link, salary, description):
        self.id_vacancy = id_vacancy
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description
        self.validate()

    def validate(self):
        if not isinstance(self.title, str):
            raise TypeError("Неверный тип данных для атрибута 'title'")
        if not isinstance(self.link, str):
            raise TypeError("Неверный тип данных для атрибута 'link'")
        if not isinstance(self.salary, (int, float)) or self.salary < 0:
            raise ValueError("Неверное значение для атрибута 'salary'")
        if not isinstance(self.description, str):
            raise TypeError("Неверный тип данных для атрибута 'description'")

    def compare_salary(self, other) -> list:
        if not isinstance(other, Vacancy):
            raise TypeError("Неверный тип данных для сравниваемого объекта")
        return self.salary - other.salary

    def __eq__(self, other) -> bool:
        """Метод сравнения вакансий"""
        if not isinstance(other, Vacancy):
            return False
        return (self.title == other.title and self.link == other.link and self.salary == other.salary and
                self.description == other.description)

    def __str__(self) -> str:
        return (f"id_vacancy:{self.id_vacancy}\nВакансия: {self.title}\n"
                f"Зарплата: {self.salary}\nОписание: {self.description}\nСсылка: {self.link}")


class VacancyFileManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy_id):
        pass


class JSONVacancyFileManager(VacancyFileManager):
    def add_vacancy(self, vacancy: Vacancy):
        with open('vacancies.json', 'a', encoding='utf-8', ) as file:
            json.dump(vars(vacancy), file, ensure_ascii=False)
            file.write('\n')

    def get_vacancies(self, criteria) -> list:

        with open('vacancies.json', 'r', encoding='utf-8') as file:
            vacancies = [json.loads(line) for line in file]
            result = []
            for data in vacancies:
                if criteria.lower() in data["title"].lower() and data["description"].lower():
                    result.append(data)
        return result

    def remove_vacancy(self, vacancy_id):
        with open('vacancies.json', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open('vacancies.json', 'w', encoding='utf-8') as file:
            for line in lines:
                vacancy = json.loads(line)
                if vacancy['id_vacancy'] != vacancy_id:
                    file.write(line)
