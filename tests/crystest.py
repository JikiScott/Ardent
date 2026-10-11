import sqlite3
import tempfile
from pathlib import Path
import db1.db as database
from decimal import Decimal
from db1.db import (
    add_crystals,
    add_firm_member,
    create_firm,
    get_crystal_balance,
    get_connection,
    get_user_firm,
)
from econ.crystals import get_crystal_equivalency, beta_equivalent
from econ.mine import mine

TEST_USER = 999999999
TEST_WORKER = 888888888

def test_crystals_and_firms():
    """Run legacy tests against an isolated temporary database."""
    original_db_path = database.DB_PATH
    with tempfile.TemporaryDirectory() as temp_dir:
        database.DB_PATH = Path(temp_dir) / "crystal_firm_test.db"
        try:
            database.initialize_database()
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
            print("\n n/a")

            # print(
            #     beta_equivalent(
            #         Decimal("10"),
            #         "ignore",
            #         "omega"
            #     )
            # )


            print("\n::: NUMERATION TEST :::")
            print("\n a number is...")

            print(
                beta_equivalent(
                    Decimal("14"),
                    "AUTOCHTHONOUS",
                    "BETA"
                )
            )

            print("\n::: CRYSDB TEST :::")

            before = get_crystal_balance(
                "user",
                TEST_USER,
                "indigenous",
                "gamma"
            )

            print("Before:", before)

            after = add_crystals(
                "user",
                TEST_USER,
                "indigenous",
                "gamma",
                Decimal("2.5")
            )

            print("Add 2.5:", after)

            stored = get_crystal_balance(
                "user",
                TEST_USER,
                "indigenous",
                "gamma"
            )

            print("Read back:", stored)

            with get_connection() as conn:
                conn.execute(
                    """
                    DELETE FROM crystal_inventory
                    WHERE owner_type = ?
                      AND owner_id = ?
                    """,
                    ("user", TEST_USER)
                )

            cleaned = get_crystal_balance(
                "user",
                TEST_USER,
                "indigenous",
                "gamma"
            )

            print("After cleanup:", cleaned)

            print("\n::: MINING to DB BRIDGE TEST :::")

            # Clear prev test inventory
            with get_connection() as conn:
                conn.execute(
                    """
                    DELETE FROM crystal_inventory
                    WHERE owner_type = ?
                      AND owner_id = ?
                    """,
                    ("user", TEST_USER)
                )

            # Mine until crystal
            while True:
                result = mine()

                if result.crystal_class is not None:
                    break

            print(
                "Mined:",
                result.quantity,
                "stone",
                result.crystal_class,
                result.grade
            )

            before_bridge = get_crystal_balance(
                "user",
                TEST_USER,
                result.crystal_class,
                result.grade
            )

            print("Before storing:", before_bridge)

            after_bridge = add_crystals(
                "user",
                TEST_USER,
                result.crystal_class,
                result.grade,
                result.quantity
            )

            print("After storing:", after_bridge)

            stored_bridge = get_crystal_balance(
                "user",
                TEST_USER,
                result.crystal_class,
                result.grade
            )

            print("Read back:", stored_bridge)

            # Clean up test inventory
            with get_connection() as conn:
                conn.execute(
                    """
                    DELETE FROM crystal_inventory
                    WHERE owner_type = ?
                      AND owner_id = ?
                    """,
                    ("user", TEST_USER)
                )

            cleaned_bridge = get_crystal_balance(
                "user",
                TEST_USER,
                result.crystal_class,
                result.grade
            )

            print("After 1st cleanup:", cleaned_bridge)

            print("\n::: MINING DISTRIBUTION TEST :::")

            class_results = {
                "tone": 0,
                "elva": 0,
                "arde": 0,
                "indigenous": 0,
                "autochthonous": 0,
                "none": 0,
            }

            grade_results = {
                "delta": 0,
                "gamma": 0,
                "beta": 0,
                "alpha": 0,
            }

            TRIALS = 100_000

            for _ in range(TRIALS):
                result = mine()

                if result.crystal_class is None:
                    class_results["none"] += 1
                else:
                    class_results[result.crystal_class] += 1
                    grade_results[result.grade] += 1
                    # Only count grade when a crystal was found



            print("\n:: CLASS DISTRIBUTION ::")

            for crystal_class, count in class_results.items():
                percentage = count / TRIALS * 100
                print(f"{crystal_class:15} {count:6}  {percentage:.2f}%")


            print("\n:: GRADE DISTRIBUTION ::")

            CRYSTALS_FOUND = TRIALS - class_results["none"]

            for grade, count in grade_results.items():
                percentage = count / CRYSTALS_FOUND * 100
                print(f"{grade:15} {count:6}  {percentage:.2f}%")

            print("\n::: FIRM TEST :::")

            # Clear previous test firm
            with get_connection() as conn:
                conn.execute(
                    """
                    DELETE FROM firms
                    WHERE owner_id = ?
                    """,
                    (TEST_USER,)
                )

            firm_id = create_firm(
                TEST_USER,
                "Test Mining Co."
            )

            print("Created firm ID:", firm_id)

            firm = get_user_firm(TEST_USER)

            print("Firm ID:", firm["firm_id"])
            print("Firm name:", firm["name"])
            print("Owner ID:", firm["owner_id"])
            print("Member role:", firm["role"])

            add_firm_member(
                firm_id,
                TEST_WORKER
            )

            worker_firm = get_user_firm(TEST_WORKER)

            print("\nWorker firm ID:", worker_firm["firm_id"])
            print("Worker firm name:", worker_firm["name"])
            print("Worker role:", worker_firm["role"])

            print("\n:: FIRM CLEANUP ::")

            with get_connection() as conn:
                conn.execute(
                    """
                    DELETE FROM firms
                    WHERE firm_id = ?
                    """,
                    (firm_id,)
                )

            firm_after_cleanup = get_user_firm(TEST_USER)
            worker_after_cleanup = get_user_firm(TEST_WORKER)

            print("Owner after cleanup:", firm_after_cleanup)
            print("Worker after cleanup:", worker_after_cleanup)

            print("\n:::CLEANUP:::")

            with get_connection() as conn:
                conn.execute(
                    """
                    DELETE FROM crystal_inventory
                    WHERE owner_type = ?
                      AND owner_id = ?
                    """,
                    ("user", TEST_USER)
                )

            cleaned = get_crystal_balance(
                "user",
                TEST_USER,
                "indigenous",
                "gamma"
            )

            with get_connection() as conn:
                conn.execute(
                    """
                    DELETE FROM firms
                    WHERE firm_id = ?
                    """,
                    (firm_id,)
                )

            firm_after_cleanup = get_user_firm(TEST_USER)

            print(
                "After cleanup:",
                firm_after_cleanup
            )

            print("Cleaned:", cleaned)
            worker_after_cleanup = get_user_firm(TEST_WORKER)

            print("Owner after cleanup:", firm_after_cleanup)
            print("Worker after cleanup:", worker_after_cleanup)
        finally:
            database.DB_PATH = original_db_path


# EMPLOY

def expect_value_error(action):
    """Pass only when the supplied action raises ValueError."""
    try:
        action()
    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError, but operation succeeded."
    )


def test_employment():
    print("\n::: EMPLOY TESTS :::")

    original_db_path = database.DB_PATH

    with tempfile.TemporaryDirectory() as temp_dir:
        database.DB_PATH = Path(temp_dir) / "employment_test.db"

        try:
            # Initialize isolated test database
            database.initialize_database()

            owner_a = 900000000000000001
            owner_b = 900000000000000002
            worker = 900000000000000003
            outsider = 900000000000000004

            # Create two test firms
            firm_a = database.create_firm(owner_a, "Test Alpha")
            firm_b = database.create_firm(owner_b, "Test Beta")

            print("Created test firms.")

            # 1. Owner can invite worker
            database.create_firm_invite(firm_a, owner_a, worker)

            invites = database.get_firm_invites(worker)

            assert len(invites) == 1
            assert invites[0]["firm_id"] == firm_a

            print("PASS1: Owner can invite worker.")

            # 2. Duplicate invitations rejected
            expect_value_error(
                lambda: database.create_firm_invite(
                    firm_a, owner_a, worker
                )
            )

            assert len(database.get_firm_invites(worker)) == 1

            print("PASS2: Duplicate invitation rejected.")

            # 3. Unauthorized hiring rejected
            expect_value_error(
                lambda: database.create_firm_invite(
                    firm_a, outsider, worker
                )
            )

            assert len(database.get_firm_invites(worker)) == 1

            print("PASS3: Unauthorized hiring rejected.")

            # 4. Multiple pending invitations allowed
            database.create_firm_invite(firm_b, owner_b, worker)

            invites = database.get_firm_invites(worker)

            assert len(invites) == 2
            assert {invite["firm_id"] for invite in invites} == {
                firm_a, firm_b
            }

            print("PASS4: Multiple pending invitations allowed.")

            # 5. Worker accepts firm A
            accepted_name = database.accept_firm_invite(worker, firm_a)

            assert accepted_name == "Test Alpha"

            membership = database.get_user_firm(worker)

            assert membership is not None
            assert membership["firm_id"] == firm_a
            assert membership["role"] == "laborer"

            print("PASS5: Worker successfully employed.")

            # 6. Competing invitations cleared
            invites = database.get_firm_invites(worker)

            assert len(invites) == 0

            print("PASS6: Competing invitations cleared.")

            # 7. Already employed users cannot receive invitations
            expect_value_error(
                lambda: database.create_firm_invite(
                    firm_b, owner_b, worker
                )
            )

            print("PASS7: Employed users cannot receive invitations.")

            # 8. Firm member listing works
            members = database.get_firm_members(firm_a)

            member_ids = {member["user_id"] for member in members}
            member_roles = {
                member["user_id"]: member["role"]
                for member in members
            }

            assert owner_a in member_ids
            assert worker in member_ids

            assert member_roles[owner_a] == "owner"
            assert member_roles[worker] == "laborer"

            print("PASS8: Firm member listing works.")

            # 9. Worker can decline an invitation
            database.create_firm_invite(firm_b, owner_b, outsider)

            invites = database.get_firm_invites(outsider)
            assert len(invites) == 1

            database.decline_firm_invite(outsider, firm_b)

            assert len(database.get_firm_invites(outsider)) == 0
            assert database.get_user_firm(outsider) is None

            print("PASS9: Invitation declined.")

            # 10. Cannot accept an invitation that does not exist
            expect_value_error(
                lambda: database.accept_firm_invite(
                    outsider, firm_a
                )
            )

            assert database.get_user_firm(outsider) is None

            print("PASS10: Uninvited employment rejected.")

            # 11. Cannot decline an invitation that does not exist
            expect_value_error(
                lambda: database.decline_firm_invite(
                    outsider, firm_a
                )
            )

            print("PASS11: Invalid invitation decline rejected.")

            # 12. Owners cannot invite themselves
            expect_value_error(
                lambda: database.create_firm_invite(
                    firm_a, owner_a, owner_a
                )
            )

            print("PASS12: Self-invitation rejected.")

            print("\nALL EMPLOY TESTS PASSED.")

        finally:
            # Restore original database path
            database.DB_PATH = original_db_path


if __name__ == "__main__":
    test_crystals_and_firms()
    test_employment()
