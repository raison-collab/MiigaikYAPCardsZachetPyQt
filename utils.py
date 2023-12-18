import datetime
import random
from datetime import timedelta

from dateutil.parser import *


class Util:
    @staticmethod
    def generate_random_card_number(interval: list[int]) -> int:
        return random.randint(interval[0], interval[1])

    @staticmethod
    def calc_time_different(t0: str, t1: str) -> timedelta:
        return parse(t1) - parse(t0)
