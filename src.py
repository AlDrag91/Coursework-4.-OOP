from pprint import pprint

from data import SiteAPIHH, JSONVacancyFileManager, Vacancy


def user_interaction():
    while True:
        print('Программа вывода вакансии с ресурсов hh.ru\n Для завершения работы - выход')
        top_n = input('Введите количество вакансий для вывода в топ N: ')
        if top_n == 'выход':
            print('Дана команда на завершение работы')
            break
        else:
            params = {'per_page': top_n, 'page': 19}
            site = SiteAPIHH(params)
            x = site.make_request()
            id_vacancy = 0
            storage = JSONVacancyFileManager()
            for i in x:
                title = i['name']
                link = i['alternate_url']

                if i['salary'] is None:
                    salary = 0
                else:
                    salary = i['salary']['from']
                if salary is None:
                    salary = 0
                description = i['snippet']['responsibility']
                if description is None:
                    description = 'Нет описания'
                id_vacancy += 1
                vacancy = Vacancy(id_vacancy, title, link, salary, description)

                storage.add_vacancy(vacancy)

            print('Запрос с ресурса выполнен')
            print('Запись вакансий произведена')
            criteria = input('Введите ключевое слово для подбора: ')
            if criteria == 'выход':
                print('Дана команда на завершение работы')
                break
            else:
                rez = storage.get_vacancies(criteria)
                pprint(rez)
            while True:
                custom_deletion = int(input('Изменить ключевое слово? Да-1, Нет-2: '))
                if custom_deletion == 1:
                    criteria = input('Введите ключевое слово для подбора: ')
                    rez = storage.get_vacancies(criteria)
                    pprint(rez)
                else:
                    break

            while True:
                custom_deletion = int(input('Произвести удаление вакансии? Да-1, Выход-2: '))
                if custom_deletion == 1:
                    custom_deletion = int(input('Введите id_vacancy'))
                    storage.remove_vacancy(custom_deletion)
                    print('Удаление применено')
                    rez = storage.get_vacancies(criteria)
                    pprint(rez)
                elif custom_deletion == 2:
                    break
