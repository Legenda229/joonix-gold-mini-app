from config import DEFAULT_RATE, REJECTION_COMPENSATION


def calc_price(gold: int, rate: float = DEFAULT_RATE) -> float:
    return round(gold * rate, 2)


def calc_listing_price(gold: int, rate: float = DEFAULT_RATE) -> float:
    return round(gold * rate * 1.20, 2)


def get_compensation(gold_amount: int) -> int:
    if 100 <= gold_amount <= 199:
        return REJECTION_COMPENSATION["100-199"]
    if 200 <= gold_amount <= 399:
        return REJECTION_COMPENSATION["200-399"]
    if gold_amount >= 400:
        return REJECTION_COMPENSATION["400+"]
    return 0
