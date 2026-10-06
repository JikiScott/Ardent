# econ/crystals.py
from decimal import Decimal
# Definitions
CRYSTAL_CLASSES = (
    "autochthonous",
    "indigenous",
    "arde",
    "elva",
    "tone",
)

CRYSTAL_GRADES = (
    "alpha",
    "beta",
    "gamma",
    "delta",
)

#Matrix

CRYSTAL_EQUIVALENCIES = {
    "autochthonous": {
        "alpha": Decimal("1.20"),
        "beta": Decimal("1.00"),
        "gamma": Decimal("0.80"),
        "delta": Decimal("0.60"),
    },
    "indigenous": {
        "alpha": Decimal("1.00"),
        "beta": Decimal("0.75"),
        "gamma": Decimal("0.60"),
        "delta": Decimal("0.50"),
    },
    "arde": {
        "alpha": Decimal("0.80"),
        "beta": Decimal("0.60"),
        "gamma": Decimal("0.50"),
        "delta": Decimal("0.40"),
    },
    "elva": {
        "alpha": Decimal("0.75"),
        "beta": Decimal("0.60"),
        "gamma": Decimal("0.50"),
        "delta": Decimal("0.30"),
    },
    "tone": {
        "alpha": Decimal("0.60"),
        "beta": Decimal("0.50"),
        "gamma": Decimal("0.30"),
        "delta": Decimal("0.10"),
    },
}

# Helper commands
def get_crystal_equivalency(crystal_class: str, grade: str) -> Decimal:
    crystal_class = crystal_class.lower()
    grade = grade.lower()

    try:
        return CRYSTAL_EQUIVALENCIES[crystal_class][grade]
    except KeyError:
        raise ValueError(
            f"Invalid crystal type: class={crystal_class}, grade={grade}"
        )


def beta_equivalent(
    quantity: Decimal,
    crystal_class: str,
    grade: str
) -> Decimal:
    multiplier = get_crystal_equivalency(crystal_class, grade)
    return quantity * multiplier