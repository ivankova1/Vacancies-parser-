class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, name, url, salary, description):
        self.name = name
        self.url = url
        self.salary = salary if salary else 0
        self.description = description


    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "descriptions": self.description
        }

    def __gt__(self, other):
        """Сравнение вакансий по зп (Меньше)"""
        return self.salary > other.salary

    def __eq__(self, other):
        """Сравнение вакансий по зп (Равны)"""
        return self.salary == other.salary

    def __str__(self):
        return (f"Вакансия: {self.name}\n"
                f"Зарплата: {self.salary}\n"
                f"Описание: {self.description}\n"
                f"Ссылка: {self.url}\n")

    def validate(self):
        """Валидация данных"""
        if not self.name or not self.url or not self.description:
            raise ValueError("Название, ссылка и описание вакансии обязательны")

        if not isinstance(self.salary, int):
            raise ValueError("Зарплата должна быть целым числом")
