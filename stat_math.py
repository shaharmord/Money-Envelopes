#- get_sd(data: List[int])
#- get_varience(data: List[int])
#- get_average(data: List[int])

import math

def get_average(data):
    if not data:
        return 0.0
    return sum(data) / len(data)

def get_variance(data):
    if not data:
        return 0.0
    mean = get_average(data)
    return sum((x - mean) ** 2 for x in data) / len(data)

def get_sd(data):
    variance = get_variance(data)
    return math.sqrt(variance)
