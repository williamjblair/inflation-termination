#!/usr/bin/env python3
"""Exact validator for the binary-triangle inflation certificates."""

from __future__ import annotations

import itertools
import json
import re
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
NAME = re.compile(r"^([ABC])(\d)(\d)$")
ROOT = re.compile(r"^D(\d)(\d)(\d)$")


def fraction(text: str) -> Fraction:
    return Fraction(text)


def root_name(i: int, j: int, k: int) -> str:
    return f"D{i}{j}{k}"


def ordering(t: int) -> list[str]:
    return (
        [f"A{i}{j}" for i in range(1, t + 1) for j in range(1, t + 1)]
        + [f"B{i}{k}" for i in range(1, t + 1) for k in range(1, t + 1)]
        + [f"C{j}{k}" for j in range(1, t + 1) for k in range(1, t + 1)]
    )


def expected_support(t: int, name: str) -> set[str]:
    match = NAME.fullmatch(name)
    assert match
    kind, x, y = match.group(1), int(match.group(2)), int(match.group(3))
    if kind == "A":
        return {root_name(x, y, k) for k in range(1, t + 1)}
    if kind == "B":
        return {root_name(x, j, y) for j in range(1, t + 1)}
    return {root_name(i, x, y) for i in range(1, t + 1)}


def p_atoms(t: int) -> dict[str, Fraction]:
    epsilon = Fraction(1, 2 * t**3)
    q = 1 - epsilon
    r = q ** (t - 1)
    result = {}
    for value in range(8):
        bits = f"{value:03b}"
        ones = bits.count("1")
        result[bits] = q * r**ones * (1 - r) ** (3 - ones)
        if bits == "000":
            result[bits] += epsilon
    return result


def swap(value: int, position: int) -> int:
    if value == position:
        return position + 1
    if value == position + 1:
        return position
    return value


def map_root(name: str, axis: int, position: int) -> str:
    match = ROOT.fullmatch(name)
    assert match
    indices = [int(match.group(i)) for i in (1, 2, 3)]
    indices[axis] = swap(indices[axis], position)
    return root_name(*indices)


def map_output(name: str, axis: int, position: int) -> str:
    match = NAME.fullmatch(name)
    assert match
    kind, x, y = match.group(1), int(match.group(2)), int(match.group(3))
    if kind == "A":
        indices = [x, y]
        if axis in (0, 1):
            indices[axis] = swap(indices[axis], position)
    elif kind == "B":
        indices = [x, y]
        if axis == 0:
            indices[0] = swap(indices[0], position)
        elif axis == 2:
            indices[1] = swap(indices[1], position)
    else:
        indices = [x, y]
        if axis == 1:
            indices[0] = swap(indices[0], position)
        elif axis == 2:
            indices[1] = swap(indices[1], position)
    return f"{kind}{indices[0]}{indices[1]}"


def probability_of_outputs(
    output_names: list[str], values: str, supports: dict[str, set[str]],
    epsilon: Fraction, q: Fraction,
) -> Fraction:
    roots = sorted(set().union(*(supports[name] for name in output_names)))
    total = Fraction(0)
    for bits in itertools.product((0, 1), repeat=len(roots)):
        assignment = dict(zip(roots, bits))
        observed = "".join(
            "1" if all(assignment[root] == 0 for root in supports[name]) else "0"
            for name in output_names
        )
        if observed != values:
            continue
        defects = sum(bits)
        total += epsilon**defects * q ** (len(roots) - defects)
    return total


def validate_structural(t: int) -> dict:
    data = json.loads((HERE / f"t{t}-defect.json").read_text())
    assert data["schema"] == "inflation-defect-certificate-v1"
    assert data["order"] == t
    epsilon = fraction(data["root_law"]["p_one"])
    q = fraction(data["root_law"]["p_zero"])
    assert data["root_law"]["kind"] == "iid-bernoulli"
    assert epsilon == Fraction(1, 2 * t**3)
    assert q == 1 - epsilon
    assert 0 < epsilon < 1 and 0 < q < 1
    assert fraction(data["r"]) == q ** (t - 1)

    roots = {
        root_name(i, j, k)
        for i in range(1, t + 1)
        for j in range(1, t + 1)
        for k in range(1, t + 1)
    }
    assert set(data["roots"]) == roots
    assert len(data["roots"]) == t**3
    # The independent root law is normalized and nonnegative exactly:
    # sum_d epsilon^|d| q^(t^3-|d|) = (epsilon+q)^(t^3) = 1.
    assert (epsilon + q) ** (t**3) == 1

    outputs = {row["name"]: set(row["value_one_iff_all_zero"]) for row in data["outputs"]}
    assert list(row["name"] for row in data["outputs"]) == ordering(t)
    for name in ordering(t):
        assert outputs[name] == expected_support(t, name)
        assert outputs[name] <= roots

    symmetry_checks = 0
    for axis in range(3):
        for position in range(1, t):
            root_image = {map_root(root, axis, position) for root in roots}
            assert root_image == roots
            for name in ordering(t):
                mapped_support = {map_root(root, axis, position) for root in outputs[name]}
                assert mapped_support == outputs[map_output(name, axis, position)]
            symmetry_checks += 1
    assert symmetry_checks == data["claimed_symmetry_generators"]

    target = p_atoms(t)
    assert {bits: fraction(value) for bits, value in data["target_atoms"].items()} == target
    assert sum(target.values()) == 1
    assert all(value >= 0 for value in target.values())
    copied_triangle_equations = 0
    local_laws: dict[int, dict[str, Fraction]] = {}
    for i in range(1, t + 1):
        for j in range(1, t + 1):
            for k in range(1, t + 1):
                names = [f"A{i}{j}", f"B{i}{k}", f"C{j}{k}"]
                central = root_name(i, j, k)
                assert outputs[names[0]] & outputs[names[1]] == {central}
                assert outputs[names[0]] & outputs[names[2]] == {central}
                assert outputs[names[1]] & outputs[names[2]] == {central}
                law = {}
                for value in range(8):
                    bits = f"{value:03b}"
                    law[bits] = probability_of_outputs(names, bits, outputs, epsilon, q)
                    assert law[bits] == target[bits]
                    copied_triangle_equations += 1
                if i == j == k:
                    local_laws[i] = law

    diagonal_supports = {}
    for i in range(1, t + 1):
        diagonal_supports[i] = set().union(
            outputs[f"A{i}{i}"], outputs[f"B{i}{i}"], outputs[f"C{i}{i}"]
        )
        assert len(diagonal_supports[i]) == 3 * t - 2
    for i in range(1, t + 1):
        for j in range(i + 1, t + 1):
            assert diagonal_supports[i].isdisjoint(diagonal_supports[j])

    diagonal_equations = 0
    for states in itertools.product(range(8), repeat=t):
        direct = Fraction(1)
        prescribed = Fraction(1)
        for i, state in enumerate(states, 1):
            bits = f"{state:03b}"
            # Disjoint root supports make the exact joint probability the
            # product of the independently enumerated local probabilities.
            direct *= local_laws[i][bits]
            prescribed *= target[bits]
        assert direct == prescribed
        diagonal_equations += 1
    assert diagonal_equations == data["claimed_diagonal_equations"]

    p000 = target["000"]
    p0 = sum(value for bits, value in target.items() if bits[0] == "0")
    assert p0 == 1 - q**t
    gap = p000**2 - p0**3
    lower_bound = epsilon**2 / 2
    assert gap >= lower_bound > 0
    if t >= 2:
        assert all(value > 0 for value in target.values())
    return {
        "order": t,
        "root_count": t**3,
        "observed_count": 3 * t**2,
        "symmetry_generators": symmetry_checks,
        "copied_triangle_equations": copied_triangle_equations,
        "diagonal_equations": diagonal_equations,
        "finner_gap": f"{gap.numerator}/{gap.denominator}",
        "uniform_lower_bound": f"{lower_bound.numerator}/{lower_bound.denominator}",
    }


def assignment_image(key: str, names: list[str], axis: int, position: int) -> str:
    source = dict(zip(names, key))
    image = {map_output(name, axis, position): bit for name, bit in source.items()}
    return "".join(image[name] for name in names)


def full_lp_errors(path: Path) -> tuple[list[str], dict]:
    data = json.loads(path.read_text())
    errors: list[str] = []
    t = data.get("order")
    names = data.get("ordering", [])
    denominator = data.get("denominator", 0)
    rows = data.get("entries", [])
    weights = {}
    if t != 2:
        errors.append("order")
    if names != ordering(2):
        errors.append("ordering")
    if not isinstance(denominator, int) or denominator <= 0:
        errors.append("denominator")
    for row in rows:
        key, numerator = row.get("assignment"), row.get("numerator")
        if not isinstance(key, str) or len(key) != 12 or set(key) - {"0", "1"}:
            errors.append("assignment")
            continue
        if key in weights:
            errors.append("duplicate assignment")
        if not isinstance(numerator, int) or numerator < 0:
            errors.append("nonnegativity")
        weights[key] = numerator
    if data.get("implicit_unlisted_numerator") != 0:
        errors.append("implicit coordinates")
    if sum(weights.values()) != denominator:
        errors.append("normalization")

    symmetry_equations = 0
    if denominator > 0 and names == ordering(2):
        for axis in range(3):
            for key_tuple in itertools.product("01", repeat=12):
                key = "".join(key_tuple)
                image = assignment_image(key, names, axis, 1)
                if weights.get(key, 0) != weights.get(image, 0):
                    errors.append(f"symmetry axis {axis}")
                    break
                symmetry_equations += 1

    diagonal_equations = 0
    if denominator > 0 and names == ordering(2):
        index = {name: position for position, name in enumerate(names)}
        diagonal_positions = [
            index["A11"], index["B11"], index["C11"],
            index["A22"], index["B22"], index["C22"],
        ]
        marginal = {"".join(bits): 0 for bits in itertools.product("01", repeat=6)}
        for key, numerator in weights.items():
            diagonal = "".join(key[position] for position in diagonal_positions)
            marginal[diagonal] += numerator
        target = p_atoms(2)
        for bits, numerator in marginal.items():
            prescribed = target[bits[:3]] * target[bits[3:]]
            if Fraction(numerator, denominator) != prescribed:
                errors.append(f"diagonal {bits}")
            diagonal_equations += 1
    return errors, {
        "nonzero_coordinates": sum(value > 0 for value in weights.values()),
        "normalization_numerator": sum(weights.values()),
        "denominator": denominator,
        "symmetry_equations": symmetry_equations,
        "diagonal_equations": diagonal_equations,
        "nonnegative": all(value >= 0 for value in weights.values()),
    }


def main() -> int:
    structural = [validate_structural(t) for t in (1, 2, 3)]
    good_errors, full = full_lp_errors(HERE / "t2-full-lp.json")
    assert not good_errors, good_errors
    bad_errors, bad = full_lp_errors(HERE / "t2-corrupted-negative-control.json")
    assert bad["normalization_numerator"] == bad["denominator"]
    assert bad["nonnegative"]
    assert bad_errors
    assert any(error.startswith("diagonal ") for error in bad_errors)
    result = {
        "status": "PASS",
        "structural_certificates": structural,
        "t2_full_lp": full,
        "negative_control": {
            "normalization_preserved": True,
            "nonnegativity_preserved": True,
            "rejected": True,
            "first_error": bad_errors[0],
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
