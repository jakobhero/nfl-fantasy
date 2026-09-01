# GitHub Actions Workflows

## Draft Order Generation

The `draft-order.yml` workflow draws the draft order for the season named in `data/season.txt`.

### Trigger Conditions
The draw runs when a pull request carrying the **`draw-order`** label is merged into `main`.

It is deliberately not coupled to a file changing. Triggering on edits to `data/players.csv` meant that any roster edit — fixing a typo, renaming a team mid-season — would redraw the order and commit over it, and that a run failing for an unrelated reason left nothing to retrigger it, because the roster had already landed. The label makes the draw something someone explicitly asked for, and it survives squash and rebase merges, which a branch-name convention would not.

To rerun a draw that failed for an infrastructure reason, use Re-run jobs on the run itself — it replays the same merge event.

### What It Does
1. **Sets up the environment**: uv provisions the Python pinned in `.python-version` plus the locked dependencies
2. **Generates a seed**: Combines the merge commit hash and the runtime timestamp
3. **Runs draft order generation**: Executes `draft_order.py` with the generated seed, which records the seed next to the order it produced
4. **Logs all information**: Prints commit hash, timestamp, seed, and draft order output
5. **Commits changes**: Commits everything under `data/<season>/`

### Permissions
The workflow needs `contents: write` to push its commit. The repository default for the workflow token is read-only, under which the `git push` fails fatally with exit code 128.

Because the trigger is a closed pull request, the checkout has to name `base.ref` explicitly. `github.ref` points at the pull request's merge ref on that event, which cannot be pushed to.

### Seed Generation
The seed is generated as follows:
- Takes the first 8 characters of the merge commit hash
- Converts it to decimal
- Adds the current Unix timestamp
- Because the timestamp is part of it, the seed differs on every run. What makes a draw reproducible after the fact is the seed being committed to `data/<season>/seed.txt`.

### Files Modified
- `data/<season>/draft_order.csv` - The drawn order
- `data/<season>/seed.txt` - The season seed, reused by the division and schedule draws

### Redraw Protection
A season that has been drawn is final: `draft_order.py` exits rather than overwrite an existing `data/<season>/seed.txt`. This holds no matter how the workflow was started, which a trigger alone cannot guarantee. To draw again, either bump `data/season.txt` to a new season or pass `--force` deliberately.

### Division and Schedule Draws
These stay out of CI and are run locally after pulling the workflow's commit. They read `data/<season>/seed.txt`, so they use the same CI-drawn season seed without it having to be copied out of the workflow logs. Each draw salts the seed differently — see `season_seed.py`.
