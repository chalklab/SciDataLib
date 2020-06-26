def is_number(n):
    """Function used for determining datatype"""

    try:
        float(n)
    except ValueError:
        return False
    return True