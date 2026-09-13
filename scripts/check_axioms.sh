#!/usr/bin/env bash
# Verification gate for this repository.
#
# Fails if:
#   1. any Lean source under TriangleInflation/ or PalomarSolutions/ contains a literal
#      `sorry` or `admit` (the Challenge is allowed its one `sorry`, by Palomar's rule), or
#   2. the Challenge does not contain exactly one `sorry`, or
#   3. Palomar/TriangleInflation/Challenge.lean is stale with respect to
#      TriangleInflation/Defs.lean, or
#   4. Audit.lean reports `sorryAx` for any audited theorem, or
#   5. any audited theorem depends on an axiom outside the allowed kernel set.
#
# Run from the repository root:
#   lake build && bash scripts/check_axioms.sh
set -euo pipefail

ALLOWED='[propext, Classical.choice, Quot.sound]'
CHALLENGE='Palomar/TriangleInflation/Challenge.lean'
fail() { echo "FAIL: $*" >&2; exit 1; }

# 1. No literal sorry / admit in the library or in the Solution.
for proof_dir in TriangleInflation PalomarSolutions; do
  if grep -rnoE --include='*.lean' '\b(sorry|admit)\b' "$proof_dir" ; then
    fail "literal sorry/admit in $proof_dir/"
  fi
done
if grep -noE '\b(sorry|admit)\b' TriangleInflation.lean Audit.lean ; then
  fail "literal sorry/admit in a root module"
fi

# 2. The Challenge states the theorem and leaves it open, exactly once.
challenge_sorries="$(grep -coE '\bsorry\b' "$CHALLENGE" || true)"
[ "$challenge_sorries" = "1" ] || fail "$CHALLENGE has $challenge_sorries sorry, expected 1"

# 3. The Challenge's definitions are still the library's definitions.
python3 scripts/gen_challenge.py --check || fail "$CHALLENGE is stale"

# 4/5. Build the audit and inspect the axiom report.
report="$(lake env lean Audit.lean 2>&1)"
echo "$report"

echo "$report" | grep -qiE '(^| )error' && fail "Audit.lean did not compile cleanly"
echo "$report" | grep -q 'sorryAx'        && fail "an audited theorem depends on sorryAx"

# Every "depends on axioms:" report must be a subset of the allowed kernel set. Lean may
# wrap the axiom list across several lines for long theorem names, so collect continuation
# lines until the closing bracket appears.
seen=0
while IFS= read -r line; do
  if [[ "$line" == *"depends on axioms:"* ]]; then
    seen=$((seen+1))
    axioms="${line#*depends on axioms: }"
    while [[ "$axioms" != *"]"* ]]; do
      IFS= read -r continuation || fail "unterminated axiom report -> $line"
      axioms+="$continuation"
    done
    compact="$(printf '%s' "$axioms" | tr -d '[][:space:]')"
    if [ -n "$compact" ]; then
      IFS=',' read -r -a axiom_names <<< "$compact"
      for axiom in "${axiom_names[@]}"; do
        case "$axiom" in
          propext|Classical.choice|Quot.sound) ;;
          *) fail "unexpected axiom '$axiom' -> $line" ;;
        esac
      done
    fi
  fi
done <<< "$report"

[ "$seen" -gt 0 ] || fail "no axiom report produced (is Audit.lean wired up?)"
echo "PASS: $seen audited theorem(s) clean, axioms subset of $ALLOWED"
