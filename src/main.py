import json
from utils import HHAPI, SuperJobAPI
from vacancies import Vacancy
from JSON_SAVE import JSONFileHeandler
from config import SUPERJOB_API_KEY

# Константы для выбора платформы
PLATFORM_HH = '1'
PLATFORM_SJ = '2'

def choose_platform():
    """Выбор платформы для поиска вакансий."""
    platform = input("Выберите платформу для поиска вакансий (1 - HeadHunter, 2 - SuperJob): ")
    if platform == PLATFORM_HH:
        return HHAPI()
    elif platform == PLATFORM_SJ:
        return SuperJobAPI(SUPERJOB_API_KEY)
    else:
        print("Неверный выбор платформы.")
        return None

def get_vacancies(api, platform, keyword):
    """Получение вакансий с учетом нескольких страниц."""
    vacancies_data = []
    page = 0
    while True:
        if platform == PLATFORM_HH:
            new_vacancies = api.get_vacancies(keyword, per_page=100, page=page)
        elif platform == PLATFORM_SJ:
            new_vacancies = api.get_vacancies(keyword, count=100, page=page)

        if not new_vacancies:
            break

        vacancies_data.extend(new_vacancies)
        page += 1

    return vacancies_data

def create_vacancy_objects(platform, vacancies_data, keyword):
    """Создание списка объектов Vacancy."""
    vacancies = []
    for item in vacancies_data:
        if platform == PLATFORM_HH:
            name = item.get('name', 'Название не указано')
            url = item.get('alternate_url', 'Ссылка не доступна')
            salary = item.get('salary', {}).get('from', 0) if item.get('salary') else 0
            snippet = item.get('snippet', {})
            description = snippet.get('requirement', '') if snippet else ''
            description = description.lower() if description else ''

        elif platform == PLATFORM_SJ:
            name = item.get('profession', 'Название не указано')
            url = item.get('link', 'Ссылка не доступна')
            salary = item.get('payment_from', 0)
            description = item.get('candidat', '')

            full_description = item.get('vacancyRichText', '') if item.get('vacancyRichText') else ''
            company_name = item.get('firm_name', '') if item.get('firm_name') else ''
            keywords = ' '.join(item.get('keywords', [])) if item.get('keywords') else ''

            full_text = f"{description} {full_description} {company_name} {keywords}".lower()
            description = full_text[:500] if len(full_text) > 500 else full_text

        if keyword in name.lower() or keyword in description:
            vacancies.append(Vacancy(name, url, salary, description))

    return vacancies



def filter_vacancies_by_salary(vacancies, min_salary_input):
    """Фильтрация вакансий по зарплате."""
    if min_salary_input:
        try:
            min_salary = int(min_salary_input)
            return [vacancy for vacancy in vacancies if vacancy.salary >= min_salary]
        except ValueError:
            print("Некорректный ввод. Минимальная зарплата будет установлена в 0.")
    return vacancies

def filter_vacancies_by_keywords(vacancies, filter_keywords_input):
    """Фильтрация вакансий по ключевым словам."""
    if filter_keywords_input:
        filter_keywords = [keyword.strip().lower() for keyword in filter_keywords_input.split(',')]
        return [vacancy for vacancy in vacancies if any(kw in vacancy.description.lower() for kw in filter_keywords)]
    return vacancies

def save_vacancies_to_file(vacancies, filename):
    """Сохранение вакансий в файл."""
    if vacancies:
        file_handler = JSONFileHeandler(filename)
        vacancies_list = [vacancy.to_dict() for vacancy in vacancies]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies_list, f, ensure_ascii=False, indent=4)
        print(f"Результаты сохранены в файл {filename}.")
    else:
        print("Нет вакансий, соответствующих вашим критериям.")

def user_iteration():
    """Основная функция для взаимодействия с пользователем."""
    api = choose_platform()
    if not api:
        return

    api.connect()

    keyword = input("Введите поисковый запрос: ").lower()
    platform = PLATFORM_HH if isinstance(api, HHAPI) else PLATFORM_SJ

    vacancies_data = get_vacancies(api, platform, keyword)
    print(f"Получено {len(vacancies_data)} вакансий.")

    vacancies = create_vacancy_objects(platform, vacancies_data, keyword)

    min_salary_input = input("Введите минимальную зарплату (или нажмите Enter для пропуска): ")
    filtered_vacancies = filter_vacancies_by_salary(vacancies, min_salary_input)

    filter_keywords_input = input("Введите ключевые слова для фильтрации вакансий (через запятую, или нажмите Enter для пропуска): ")
    final_vacancies = filter_vacancies_by_keywords(filtered_vacancies, filter_keywords_input)

    final_vacancies.sort(key=lambda x: x.salary, reverse=True)

    num_vacancies_input = input("Сколько вакансий вы хотите получить? (или нажмите Enter для получения всех): ")
    if num_vacancies_input:
        try:
            num_vacancies = int(num_vacancies_input)
            if num_vacancies > 0:
                final_vacancies = final_vacancies[:num_vacancies]
            else:
                print("Количество должно быть больше 0. Будут показаны все вакансии.")
        except ValueError:
            print("Некорректный ввод. Будут показаны все вакансии.")


    filename = input("Введите имя файла для сохранения результатов: ") + ".json"
    save_vacancies_to_file(final_vacancies, filename)

if __name__ == "__main__":
    user_iteration()