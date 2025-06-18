"""
Write function which receives list of integers. Calculate power of each integer and
subtract difference between original previous value and it's power. For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3])
    [1, 4, 7]  # because [1^2, 2^2 - (1^2 - 1), 3^2 - (2^2 - 2)]
"""

from typing import List


def calculate_power_with_difference(ints: List[int]) -> List[int]:
    results_list = []
    prev_substract = 0
    for current_int in ints:
        current_power = current_int**2
        results_list.append(current_power - prev_substract)
        prev_substract = current_power - current_int
    return results_list


print(calculate_power_with_difference([1, 2, 3]))
