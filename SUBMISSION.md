# Submitting these statements to Palomar

Nothing in this repository submits anything, and nothing in it has been pushed anywhere.
This file is the remaining checklist, for the author to work through by hand. Every step
below is a deliberate act: creating a public repository, pushing it, and registering a
record that other people will cite.

The certificate artifact now lives at `artifact/` next to `paper/`, so the replay commands of Section 16 run from this repository's root. Everything mechanical is already done. `lake build && bash scripts/check_axioms.sh` passes;
`formalization.yaml` validates against the live v0.4 schema; both Challenges regenerate
byte-identically from the library definition files.

## 0. Before anything is public

- [ ] Read `paper/main.pdf` Sections 3 to 7 once more. They are the newest material, they
      have had no external reader, and the classification is the headline of both the paper
      and the first registry entry.
- [ ] Re-read `PORTING.md`. It is the only record of how this repository differs from the
      working repository, and it is the thing a reader would check first.
- [ ] Decide whether the two statements go in as two records or one. The submission form
      takes a single Comparator config path, and this repository has two configs, one per
      Challenge. Two records is the reading that matches the form; confirm it against
      https://palomar-registry.org/how-to-submit before submitting, and if one record can
      carry both, submit the classification config and name the triangle theorem in the
      metadata.

## 1. Create the public repository

- [ ] Create the public GitHub repository `williamjblair/inflation-termination`. That is the
      URL the manuscript already cites (the macro `\repourl` in `paper/main.tex`, one line
      to change if you pick another name or account; the abstract, the introduction,
      Section 16, Appendix B and the code-availability paragraph all use it). Renaming after
      registration is not free, because the record pins a repository URL.
- [ ] `git remote add origin git@github.com:williamjblair/inflation-termination.git`
- [ ] `git push -u origin main`
- [ ] Confirm that `paper/main.pdf` and the LaTeX sources are content you are willing to
      have public before the arXiv posting. This repository is meant to precede the
      preprint; `paper/release/RELEASE_STATUS.md` records that the manuscript has not been
      posted or submitted anywhere.
- [ ] Record the full 40-character commit SHA of the pushed `main`. Palomar pins that exact
      commit, so any later change needs a new version of the record.

## 2. Check the submission requirements once against the published standard

Palomar's stated minimum is a Lean project with one lakefile, a pinned `lean-toolchain`, a
short Challenge module stating the result, a Solution module proving it, a `comparator.json`
naming every theorem to compare, a `formalization.yaml` with metadata, and a licence file.
All seven are present. Two points to re-check against the current published policy, since
both have moved before:

- [ ] The permitted-axiom policy. Both configs permit `propext`, `Quot.sound` and
      `Classical.choice`, and the audit shows nothing else is used.
- [ ] The Mathlib requirement. The pin `db584cd6d46c92f209a44c0f1c829460d327499d` is a
      commit on canonical `master`, which is what Palomar requires. Do not move it: the
      whole development has been checked at that commit and at Lean `v4.33.0`.

## 3. Comparator, run locally

Done, 2026-09-14, both pairs, both `Your solution is okay!` with the Lean default kernel
accepting each solution. Nothing here is blocked on it. Repeat it after any change to a
Challenge, a Solution or a definitions file:

```bash
lake build
COMPARATOR_LANDRUN=<comparator>/scripts/fake-landrun.sh \
COMPARATOR_LEAN4EXPORT=<lean4export built at v4.33.0>/.lake/build/bin/lean4export \
  lake env <comparator>/.lake/build/bin/comparator \
  Palomar/TriangleInflation/classification-comparator.json
# and again for Palomar/TriangleInflation/comparator.json
```

Two things cost time the first time and are worth knowing:

- `lean4export` must be built at **this** repository's Lean version. A binary built at
  `v4.33.1` refuses the `v4.33.0` oleans with `failed to read file ... incompatible header`.
  Clone https://github.com/leanprover/lean4export, write `leanprover/lean4:v4.33.0` into its
  `lean-toolchain`, and `lake build`.
- On macOS there is no `landrun`, so Comparator's own `scripts/fake-landrun.sh` stands in.
  It execs the command unsandboxed. That tests the comparison and not the isolation, which
  is fine for debugging and is exactly why the registry runs its own check.

If Comparator ever does complain, the likeliest cause is a constant that the Challenge
carries and the Solution does not define identically. The classification Challenge carries a
*selection* of `TriangleInflation/Graph/Defs.lean` rather than the whole file, so the fix is
to add the missing declaration head to `GRAPH_EXTRACT` in `scripts/gen_challenge.py` and
regenerate.

## 4. Submit

The submission is a web form at https://submit.palomar-registry.org/. It asks for the public
repository URL, the full 40-character commit SHA, optionally a Comparator config path, and a
declaration of your relationship to the formalization (here: maintainer and author). It
authenticates by GitHub sign-in, to check push permission, and then discards the token.

- [ ] Submit the classification config path `Palomar/TriangleInflation/classification-comparator.json`.
- [ ] Wait. Mechanical verification runs in a public GitHub Actions workflow, and editorial
      review follows if it passes, with a stated target of about an hour. The results appear
      only on a private status page, so keep that page's URL.
- [ ] Read the review before deciding. The submission is not public until you register it;
      the alternatives are to register or to withdraw.
- [ ] Register. Copy the entry page URL from the address bar, and record both the Palomar ID
      and the version, in the form `PALOMAR-YYYY-MM-DD-NNNNNN v1`. A bare ID resolves to the
      newest version of the record, so a citation has to name the version.
- [ ] Repeat for `Palomar/TriangleInflation/comparator.json` if the two statements are going
      in as two records.

There is an agent protocol documented at https://submit.palomar-registry.org/llms.txt, with
`POST /api/submit`, a GitHub tag-and-gist challenge, `POST /api/verify`, `GET /api/submission`,
`GET /api/review` and finally `POST /register` or `POST /withdraw`. Use the web form unless
you have a reason not to: the final `POST /register` is the act that makes the record public,
and it should be yours.

## 5. Put the entry ids into the paper

Once the ids exist, the formal-verification paragraph of Section 16
(`paper/sections/11-reproducibility.tex`) needs two sentences. The paragraph currently ends
with "The Lean sources accompany the artifact." Replace that sentence with, filling in the
two ids and the repository URL:

> The Lean sources accompany the artifact and are also public at
> \url{https://github.com/willblair0708/NAME}. Two statements are registered with Palomar,
> the registry of machine-checked Lean results, which re-runs the comparison between the
> advertised statement and its proof on its own infrastructure: Theorem~\ref{thm:classification}
> as \texttt{PALOMAR-YYYY-MM-DD-NNNNNN v1} and Theorem~\ref{thm:main} as
> \texttt{PALOMAR-YYYY-MM-DD-MMMMMM v1}.

Then:

- [ ] Recompile `paper/main.tex` and rebuild `release/arxiv-src/` in the working repository.
- [ ] Copy the refreshed `paper/` back into this repository, commit, push, and submit a new
      *version* of each Palomar record against the new commit, using the `existing_id` field
      so that the records stay linked rather than becoming duplicates.
- [ ] Update `paper/release/RELEASE_STATUS.md`: the `LEAN_STATUS` line still says the
      registry repository is held and unsynced, and `NEXT_SINGLE_HIGHEST_VALUE_ACTION` still
      names this sync.

## What is deliberately not here

- The square witness of Theorem 6.11 is unproved and is not in this repository at all. It is
  recorded as unproved in `paper/release/NONCLAIMS.md` and in the Coverage table of
  `README.md`. Do not let a reader infer from a green build that it is proved.
- No claim of firstness. `paper/release/PRIORITY_AUDIT.md` records `PRIORITY_NOT_KILLED` and
  says so explicitly, and `formalization.yaml` repeats it under `review.notes`.
- No independent human review of the mathematics. `review.status` is `self-assessed`.
