def sumvalues(values):
    total = 0
    try:
        for num in values:
            total += num
        return total
    except:
        raise ValueError(
            "value error, check input for non-numerical values")


def maxvalue(values):
    current_max = values[0]
    try:
        for num in values:
            if num > current_max:
                current_max = num
        return current_max
    except:
        raise ValueError(
            "value error, check input for non-numerical values")


def minvalue(values):
    current_min = values[0]
    try:
        for num in values:
            if num < current_min:
                current_min = num
        return current_min
    except:
        raise ValueError(
            "value error, check input for non-numerical values")


def meannvalue(values):
    # if not is int or float: raise instance
    total = 0
    count = 0
    for val in values:
        try:
            total += val
        except:
            raise ValueError(
                "value error, check input for non-numerical values")
        count += 1
    return total / count


def countvalue(values, x):
    count = 0
    for val in values:
        if val == x:
            count += 1
    return count
