#!/usr/bin/env bash
# Verification gate for this repository.
#
# Fails if:
#   1. any Lean source under TriangleInflation/ or PalomarSolutions/ contains a literal
#      `sorry` or `admit` (each Challenge is allowed its one `sorry`, by Palomar's rule), or
#   2. a Challenge does not contain exactly one `sorry`, or
#   3. a Challenge is stale with respect to the library definitions it carries
#      (TriangleInflation/Defs.lean and TriangleInflation/Graph/Defs.lean), or
#   4. Audit.lean reports `sorryAx` for any audited declaration, or
#   5. any audited declaration depends on an axiom outside the allowed kernel set.
#
# Run from the repository root:
#   lake build && bash scripts/check_axioms.sh
set -euo pipefail

ALLOWED='[propext, Classical.choice, Quot.sound]'
CHALLENGES=(
  'Palomar/TriangleInflation/Challenge.lean'
  'Palomar/TriangleInflation/ClassificationChallenge.lean'
)
fail() { echo "FAIL: $*" >&2; exit 1; }

# 1. No literal sorry / admit in the library or in the Solutions.
for proof_dir in TriangleInflation PalomarSolutions; do
  if grep -rnoE --include='*.lean' '\b(sorry|admit)\b' "$proof_dir" ; then
    fail "literal sorry/admit in $proof_dir/"
  fi
done
if grep -noE '\b(sorry|admit)\b' TriangleInflation.lean Audit.lean ; then
  fail "literal sorry/admit in a root module"
fi

# 2. Each Challenge states its theorem and leaves it open, exactly once.
for challenge in "${CHALLENGES[@]}"; do
  challenge_sorries="$(grep -coE '\bsorry\b' "$challenge" || true)"
  [ "$challenge_sorries" = "1" ] \
    || fail "$challenge has $challenge_sorries sorry, expected 1"
done

# 3. Both Challenges carry the library's current definitions.
python3 scripts/gen_challenge.py --check || fail "a Challenge is stale"

# 4/5. Build the audit and inspect the axiom report.
report="$(lake env lean Audit.lean 2>&1)"
echo "$report"

echo "$report" | grep -qiE '(^| )error' && fail "Audit.lean did not compile cleanly"
echo "$report" | grep -q 'sorryAx'        && fail "an audited declaration depends on sorryAx"

# Every "depends on axioms:" report must be a subset of the allowed kernel set. Lean may
# wrap the axiom list across several lines for long declaration names, so collect
# continuation lines until the closing bracket appears.
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
echo "PASS: $seen audited declaration(s) clean, axioms subset of $ALLOWED"
