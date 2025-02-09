from utils import HHruAPI, SuperJobAPI
from vacancies import Vacancy
from JSON_SAVE import JSONFileHeandler

def user_iteration():
    # Выбор платформы
    platform = input("Выберите платформу для поиска вакансий (1 - HeadHunter, 2 - SuperJob): ")
    if platform == '1':
        api = HHruAPI()
    elif platform == '2':
        api_key = input("Введите ваш API ключ для SuperJob: ")
        api = SuperJobAPI(api_key)
    else:
        print("Неверный выбор платформы.")
        return

    # Подключение к API
    api.connect()

    # Ввод поискового запроса
    keyword = input("Введите поисковый запрос: ")

    # Получение вакансий
    vacancies_data = api.get_vacancy(keyword)
    vacancies = [
        Vacancy(
            item['name'],
            item['alternate_url'],
            item.get('salary', {}).get('from', 0) if item.get('salary') else 0,  # Проверка на None
            item.get('snippet', {}).get('requirement', '')
        )
        for item in vacancies_data
    ]

    # Фильтрация по зарплате
    min_salary_input = input("Введите минимальную зарплату (или нажмите Enter для пропуска): ")
    if min_salary_input:  # Проверяем, введено ли значение
        try:
            min_salary = int(min_salary_input)
            filtered_vacancies = [vacancy for vacancy in vacancies if vacancy.salary >= min_salary]
        except ValueError:
            print("Некорректный ввод. Минимальная зарплата будет установлена в 0.")
            filtered_vacancies = vacancies  # Если ввод некорректен, не фильтруем
    else:
        filtered_vacancies = vacancies  # Если ничего не введено, не фильтруем

    # Фильтрация по ключевым словам
    filter_keywords_input = input("Введите ключевые слова для фильтрации вакансий (через запятую, или нажмите Enter для пропуска): ")
    if filter_keywords_input:  # Проверяем, введены ли ключевые слова
        filter_keywords = [keyword.strip() for keyword in filter_keywords_input.split(',')]
        final_vacancies = [vacancy for vacancy in filtered_vacancies if any(keyword.lower() in vacancy.descriptions.lower() for keyword in filter_keywords)]
    else:
        final_vacancies = filtered_vacancies  # Если ничего не введено, не фильтруем

    # Сортировка вакансий по зарплате в порядке убывания
    final_vacancies.sort(key=lambda x: x.salary, reverse=True)

    # Пользователь выбирает количество вакансий
    num_vacancies_input = input("Сколько вакансий вы хотите получить? (или нажмите Enter для получения всех): ")
    if num_vacancies_input:  # Проверяем, введено ли значение
        try:
            num_vacancies = int(num_vacancies_input)
            if num_vacancies > 0:
                final_vacancies = final_vacancies[:num_vacancies]  # Ограничиваем список вакансий
            else:
                print("Количество должно быть больше 0. Будут показаны все вакансии.")
        except ValueError:
            print("Некорректный ввод. Будут показаны все вакансии.")

    # Сохранение результатов в файл
    if final_vacancies:
        filename = input("Введите имя файла для сохранения результатов: ")
        file_handler = JSONFileHeandler(filename)
        for vacancy in final_vacancies:
            file_handler.add_vacancy(vacancy)
        print(f"Результаты сохранены в файл {filename}.")
    else:
        print("Нет вакансий, соответствующих вашим критериям.")

if __name__ == "__main__":
    user_iteration()
