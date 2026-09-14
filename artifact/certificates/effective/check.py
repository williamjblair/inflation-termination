#!/usr/bin/env python3
"""Exact Farkas replay and constant calibration for effective inflation."""

from __future__ import annotations

import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def coefficient(diagonal: str) -> int:
    if diagonal in {"000111", "111000"}:
        return -1
    if diagonal in {"000000", "111111"}:
        return 0
    return 1


def swap(index: int) -> int:
    return 3 - index


def mapped_name(name: str, group_mask: int) -> str:
    kind = name[0]
    first, second = int(name[1]), int(name[2])
    if kind == "A":
        if group_mask & 1:
            first = swap(first)
        if group_mask & 2:
            second = swap(second)
    elif kind == "B":
        if group_mask & 1:
            first = swap(first)
        if group_mask & 4:
            second = swap(second)
    else:
        if group_mask & 2:
            first = swap(first)
        if group_mask & 4:
            second = swap(second)
    return f"{kind}{first}{second}"


def transformed(bits: str, names: list[str], group_mask: int) -> str:
    values = {}
    for name, bit in zip(names, bits):
        values[mapped_name(name, group_mask)] = bit
    return "".join(values[name] for name in names)


def diagonal(bits: str, names: list[str], diagonal_names: list[str]) -> str:
    values = dict(zip(names, bits))
    return "".join(values[name] for name in diagonal_names)


def main() -> int:
    data = json.loads((HERE / "farkas.json").read_text())
    assert data["schema"] == "effective-inflation-order2-farkas-v1"
    assert data["inflation_order"] == 2
    names = data["variable_order"]
    diagonal_names = data["diagonal_order"]
    assert len(names) == 12 and len(set(names)) == 12
    assert len(diagonal_names) == 6

    orbit_sums = Counter()
    checked = 0
    for bits_tuple in itertools.product("01", repeat=12):
        bits = "".join(bits_tuple)
        value = sum(
            coefficient(diagonal(transformed(bits, names, group), names, diagonal_names))
            for group in range(8)
        )
        assert value >= 0
        orbit_sums[value] += 1
        checked += 1
    assert checked == data["claimed_full_assignments_checked"]
    assert min(orbit_sums) == data["claimed_minimum_orbit_sum"]
    assert data["claimed_group_elements"] == 8

    target = {key: Fraction(value) for key, value in data["target"].items()}
    assert sum(target.values()) == 1
    target_pair = {
        first + second: p * q
        for first, p in target.items()
        for second, q in target.items()
    }
    target_dual = sum(probability * coefficient(outcome) for outcome, probability in target_pair.items())
    assert target_dual == Fraction(data["claimed_target_dual_value"])
    assert target_dual == Fraction(-1, 2)

    # Fractional independent set eta=(1/2,1/2,1/2): the common fair bit has
    # three one-bit marginals and one bit of joint entropy.
    entropy_lower_bound = Fraction(3, 2) - 1
    promise = Fraction(data["regularized_kl_promise"])
    assert entropy_lower_bound == Fraction(data["certified_entropy_lower_bound"])
    assert entropy_lower_bound >= promise > 0

    k = 1
    while Fraction(9 + 2 * k, 2**k) >= promise:
        k += 1
    assert k == 7
    theoretical_order = 24 * 4**k
    threshold = Fraction(1, 2**k)
    assert Fraction(12, theoretical_order) == threshold**2 / 2
    assert Fraction(9 + 2 * k, 2**k) < promise
    assert 24 * 13**4 == 685464

    result = {
        "status": "PASS",
        "calibration_order": 2,
        "full_assignments_checked": checked,
        "group_actions_per_assignment": 8,
        "orbit_sum_histogram": dict(sorted(orbit_sums.items())),
        "target_dual_value": str(target_dual),
        "farkas_separation_margin": str(-target_dual),
        "regularized_kl_lower_bound": str(entropy_lower_bound),
        "promise": str(promise),
        "dyadic_bound_k": k,
        "theoretical_dyadic_order_not_materialized": theoretical_order,
        "closed_bound_numerator": 685464,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
