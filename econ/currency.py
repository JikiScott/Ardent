# econ/currency.py

# Base unit: farthing (1/4 penny)

FARTHINGS_PER_PENNY = 4
PENNIES_PER_SHILLING = 12
SHILLINGS_PER_POUND = 20

FARTHINGS_PER_SHILLING = (
    FARTHINGS_PER_PENNY * PENNIES_PER_SHILLING
)

FARTHINGS_PER_POUND = (
    FARTHINGS_PER_SHILLING * SHILLINGS_PER_POUND
)

DENOMINATIONS = {
    "farthing": 1,
    "halfpenny": 2,
    "penny": 4,
    "sixpence": 24,
    "shilling": 48,
    "florin": 96,
    "crown": 240,
    "half_sovereign": 480,
    "sovereign": 960,
}


def to_farthings(amount: int, denomination: str = "sovereign") -> int:
# Convert a denomination into integer farthings.
    if type(amount) is not int or amount < 0:
        raise ValueError("Amount must be a nonnegative whole number.")

    denomination = denomination.lower()

    if denomination not in DENOMINATIONS:
        raise ValueError("Unknown currency denomination.")

    return amount * DENOMINATIONS[denomination]


def format_currency(farthings: int) -> str:
# Format farthings as pounds, shillings, pence and farthings.
    if type(farthings) is not int or farthings < 0:
        raise ValueError("Currency balance must be nonnegative.")

    pounds, remainder = divmod(farthings, FARTHINGS_PER_POUND)
    shillings, remainder = divmod(remainder, FARTHINGS_PER_SHILLING)
    pennies, remainder = divmod(remainder, FARTHINGS_PER_PENNY)

    return f"£{pounds} {shillings}s {pennies}d {remainder}f"