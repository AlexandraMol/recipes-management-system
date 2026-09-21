def convert_to_base(quantity, unit):
    if unit == "kg":
        return quantity * 1000, "g"

    if unit == "l":
        return quantity * 1000, "ml"

    return quantity, unit


def convert_from_base(quantity, unit):
    if unit == "g" and quantity >= 1000:
        return quantity / 1000, "kg"

    if unit == "ml" and quantity >= 1000:
        return quantity / 1000, "l"

    return quantity, unit
