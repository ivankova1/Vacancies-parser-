from abc import ABC, abstractmethod
import requests

class JobPlatformAPI(ABC):
    """Абстрактный класс для работы с API"""
    @abstractmethod
    def connect(self):
        """Метод для подключения к API"""
        pass

    @abstractmethod
    def get_vacancy(self, keyword: str) -> list:
        """Метод для получения вакансий по ключевому слову"""
        pass

class HHruAPI(JobPlatformAPI):
    """Класс для работы с API hh.ru"""
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def connect(self):
        """Метод для подключения к API hh.ru"""
        return "Подключение к API прошло успешно"

    def get_vacancy(self, keyword: str) -> list:
        """Получает список вакансий по ключевому слову."""
        params = {
            "text": keyword,
            "per_page": 100
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            print(f"Ошибка при запросе к API HeadHunter: {response.status_code}")
            return []

class SuperJobAPI(JobPlatformAPI):
    """Класс для работы с API SuperJob"""
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API ключ не может быть пустым")
        self.base_url = "https://api.superjob.ru/2.0/vacancies/"
        self.headers = {
            "X-Api_App-Id": api_key
        }

    def connect(self):
        """Метод для подключения к API SuperJob"""
        return "Подключение к API прошло успешно"

    def get_vacancy(self, keyword: str) -> list:
        """Получает список вакансий по ключевому слову."""
        params = {
            "text": keyword,
            "per_page": 100
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get('objects', [])
        else:
            print(f"Ошибка при запросе к API SuperJob: {response.status_code}")
            return []
