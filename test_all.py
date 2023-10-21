import pytest

from reporting import *
from intelligence import *

with open(f'./data/Pollution-London Marylebone Road.csv') as f:
    data = f.read().split('\n')


def test_daily_average_values():
    assert list(map(int, daily_average(data, 'MY1', 'no')[:9])) == [
        21, 11, 6, 3, 6]
