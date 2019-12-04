import os
import math
dirname = os.path.dirname(__file__)

input_range = (254032, 789860)


def meets_criteria(password):
    adjacents_count = []
    digits_to_check = password
    last_digit_checked = math.inf

    while digits_to_check > 0:
        rightmost = digits_to_check % 10

        # checking the digits decrease from right to left
        if rightmost > last_digit_checked:
            return False

        # if the rightmost digit is the same as the previous one,
        # add 1 to the latest counter
        if rightmost == last_digit_checked:
            adjacents_count[-1] += 1
        # if it is different, start a new counter at 1
        else:
            adjacents_count.append(1)

        last_digit_checked = rightmost
        digits_to_check //= 10

    if 2 in adjacents_count:
        return True
    else:
        return False


def count_valid_passwords(start, end):
    count = 0
    for i in range(start, end):
        if meets_criteria(i):
            count += 1
    return count


print(count_valid_passwords(input_range[0], input_range[1]))
