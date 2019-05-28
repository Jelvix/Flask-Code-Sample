def check_0_max(value, max_value):
    """
    Check if the value in range(0, max_value) and if it is not change to closest(0 or max_value)
    :param value: integer or float
    :param max_value: integer or float
    :return: 0 or max_value or value
    """
    if value not in range(0, max_value):
        if value <= 0:
            return 0
        else:
            return max_value
    return value

