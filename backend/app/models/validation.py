from decimal import Decimal

MAX_MONEY = Decimal("99999999999999.99")
MAX_PROGRESS = Decimal("100")


def validate_name(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("name must be a string")
    if not value.strip() or len(value) > 150:
        raise ValueError(
            "name must contain non-whitespace text and at most 150 characters"
        )
    return value


def validate_amount(key: str, value: Decimal, maximum: Decimal) -> Decimal:
    if not isinstance(value, Decimal):
        raise TypeError(f"{key} must be a Decimal")
    if not value.is_finite() or value < 0 or value > maximum:
        raise ValueError(f"{key} must be finite and between 0 and {maximum}")
    # Inspect digits instead of quantizing: validation is independent of context precision.
    digits = value.as_tuple()
    extra_places = max(0, -digits.exponent - 2)
    if extra_places and any(digits.digits[-extra_places:]):
        raise ValueError(f"{key} must have at most two decimal places")
    return value
