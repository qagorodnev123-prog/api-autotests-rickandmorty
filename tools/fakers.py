from faker import Faker

class Fake:
    def __init__(self, faker: Faker):
        self.faker = faker

    def character_random_id(self, start: int = 1, end: int = 10) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.

        :param start: Начало диапазона (включительно).
        :param end: Конец диапазона (включительно).
        :return: Случайное целое число.
        """
        return self.faker.random_int(start, end)

    def non_exist_character_id(self, start: int = 100000, end: int = 999999):
        return self.faker.random_int(start, end)

fake = Fake(faker=Faker())