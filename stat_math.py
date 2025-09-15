import math
from typing import List

def get_average(data: List[int]) -> float:
    """Return the arithmetic mean of a list of integers."""
    if not data:
        raise ValueError("Data list cannot be empty.")
    return sum(data) / len(data)

def get_varience(data: List[int]) -> float:
    """Return the variance of a list of integers."""
    if not data:
        raise ValueError("Data list cannot be empty.")
    mean = get_average(data)
    return sum((x - mean) ** 2 for x in data) / len(data)

def get_sd(data: List[int]) -> float:
    """Return the standard deviation of a list of integers."""
    return math.sqrt(get_varience(data))
