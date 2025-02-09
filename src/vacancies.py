
class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, title: str, link: str, salary: int, descriptions: str):
        self.title = title
        self.link = link
        self.salary = salary if salary else 0  # Если не указана, принимаем ее за 0
        self.descriptions = descriptions

    def __gt__(self, other):
        """Сравнение вакансий по зарплате (больше)"""
        return self.salary > other.salary

    def __eq__(self, other):
        """Сравнение вакансий по зарплате (равны)"""
        return self.salary == other.salary

    def __str__(self):
        """Строковое представление вакансии"""
        return f"{self.title} ({self.salary} руб.): {self.link}"

    def validate(self):
        """Валидация данных"""
        if not isinstance(self.salary, int):
            raise ValueError("Зарплата должна быть целым числом")
