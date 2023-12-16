import random


class Util:
    @staticmethod
    def generate_random_card_number(interval: list[int]) -> int:
        return random.randint(interval[0], interval[1])
