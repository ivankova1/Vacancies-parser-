from abc import abstractmethod, ABC
import json

class FileHandler(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавление вакансии в файл"""
        pass

    @abstractmethod
    def get_vacancy(self, criteria):
        """Получение вакансий из файла по критериям"""
        pass


class JSONFileHeandler(FileHandler):
    """Класс для работы с json - файлом"""

    def __init__(self, filename: str):
        self.filename = filename

    def add_vacancy(self, vacancy):
        data = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            pass

        data.append(vacancy.__dict__)
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


    def get_vacancy(self, criteria):
        """Получение вакансий из файла по критериям"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [item for item in data if criteria(item)]
        except FileNotFoundError:
            return []

