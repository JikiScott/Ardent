#Mine.py
import random
from dataclasses import dataclass
from decimal import Decimal
from db1.db import (
    add_crystals,
    get_user_firm,
)

CRYSTAL_CLASS_PROBABILITIES = {
    "tone": Decimal("0.50"),
    "elva": Decimal("0.125"),
    "arde": Decimal("0.037"),
    "indigenous": Decimal("0.01"),
    "autochthonous": Decimal("0.008"),
}
# Class rarity curve follows inverse cube truncated (1/125, 1/64, 1/27, etc); 32% chance of no crystal

CRYSTAL_GRADE_PROBABILITIES = {
    "delta": Decimal("0.5525"),
    "gamma": Decimal("0.25"),
    "beta": Decimal("0.125"),
    "alpha": Decimal("0.0625"),
}

#Grade rarity curve follows inverse square with remainder added to delta; no chance of no grade

@dataclass(frozen=True)
class MiningResult:
    crystal_class: str | None
    grade: str | None
    quantity: Decimal


def roll_crystal_class() -> str | None:
    roll = random.random()
    cumulative = 0.0

    for crystal_class, probability in CRYSTAL_CLASS_PROBABILITIES.items():
        cumulative += float(probability)

        if roll < cumulative:
            return crystal_class
    return None

def roll_crystal_grade() -> str:
    roll = random.random()
    cumulative = 0.0

    for grade, probability in CRYSTAL_GRADE_PROBABILITIES.items():
        cumulative += float(probability)

        if roll < cumulative:
            return grade

    return "delta"

def mine() -> MiningResult:
    crystal_class = roll_crystal_class()

    if crystal_class is None:
        return MiningResult(
            crystal_class=None,
            grade=None,
            quantity=Decimal("0")
        )
    grade = roll_crystal_grade()
    return MiningResult(
        crystal_class=crystal_class,
        grade=grade,
        quantity=Decimal("1")
        # To implement quantity variation later
        # Mining quantity is measured in stones.
        # Beta version: every successful mining roll yields exactly 1 stone.
    )

