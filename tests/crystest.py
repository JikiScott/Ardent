from decimal import Decimal

from econ.crystals import get_crystal_equivalency, beta_equivalent


print("::: Crystal equivalency tests :::")

print(
    "Autochthonous Beta:",
    get_crystal_equivalency("autochthonous", "beta")
)

print(
    "Autochthonous Alpha:",
    get_crystal_equivalency("autochthonous", "alpha")
)

print(
    "Tone Delta:",
    get_crystal_equivalency("tone", "delta")
)


print("\n::: Beta-equivalent conversion tests :::")

print(
    "10 stone Autochthonous Beta:",
    beta_equivalent(
        Decimal("10"),
        "autochthonous",
        "beta"
    )
)

print(
    "10 stone Autochthonous Alpha:",
    beta_equivalent(
        Decimal("10"),
        "autochthonous",
        "alpha"
    )
)

print(
    "10 stone Indigenous Gamma:",
    beta_equivalent(
        Decimal("10"),
        "indigenous",
        "gamma"
    )
)

print(
    "10 stone Tone Delta:",
    beta_equivalent(
        Decimal("10"),
        "tone",
        "delta"
    )
)

print("\n::: FAIL TEST :::")

print(
    beta_equivalent(
        Decimal("10"),
        "ignore",
        "omega"
    )
)

print(
    beta_equivalent(
        Decimal("10"),
        "banana",
        "omega"
    )
)

print("\n::: FINAL TEST :::")

print(
    beta_equivalent(
        Decimal("14"),
        "AUTOCHTHONOUS",
        "BETA"
    )
)

