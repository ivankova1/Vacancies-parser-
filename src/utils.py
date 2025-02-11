from abc import ABC, abstractmethod
import requests


class JobPlatformAPI(ABC):
    pass

    @abstractmethod
    def connect(self):
        """Метод для подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """Меотод для получения вакансий по ключевому слову"""
        pass


class HHAPI(JobPlatformAPI):
    """Класс для работы с API HH.ru"""

    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def connect(self):
        """Подключение к API HH.ru"""
        print("Подключение к API установлено")


    def get_vacancies(self, keyword: str, per_page=100, page=0):
        params = {
            "text": keyword,       # Ключевое слово для поиска
            "per_page": per_page,  # Количество вакансий на странице
            "page": page           # Номер страницы
        }
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])  # Возвращаем список вакансий
        else:
            print(f"Ошибка при запросе к API HeadHunter: {response.status_code}")
            return []

class SuperJobAPI(JobPlatformAPI):

    def __init__(self, api_key: str):
        self.base_url = "https://api.superjob.ru/2.0/vacancies/"
        self.headers = {
            "X-Api-App-Id": api_key
        }

    def connect(self):
        """Подключение к API SuperJob"""
        print("Подключение к API установлено")

    def get_vacancies(self, keyword: str, count=100, page=0):
        params = {
            "keyword": keyword,  # Ключевое слово для поиска
            "count": count,      # Количество вакансий на странице
            "page": page         # Номер страницы
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data.get('objects', [])  # Возвращаем список вакансий
        else:
            print(f"Ошибка при запросе к API SuperJob: {response.status_code}")
            return []
