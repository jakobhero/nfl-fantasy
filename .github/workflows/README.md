# GitHub Actions Workflows

## Draft Order Generation

The `draft-order.yml` workflow automatically generates a new draft order whenever the `data/players.csv` file is modified.

### Trigger Conditions
- Push to `main` or `master` branch that includes changes to `data/players.csv`

The draw deliberately does not run on pull requests — the order is only drawn once the roster has landed on `main`.

### Permissions
The workflow needs `contents: write` to push its commit. The repository default for the workflow token is read-only, under which the `git push` fails fatally with exit code 128.

### What It Does
1. **Sets up the environment**: Python 3.9 + Poetry with all dependencies
2. **Generates a deterministic seed**: Combines commit hash and runtime timestamp
3. **Runs draft order generation**: Executes `draft_order.py` with the generated seed
4. **Logs all information**: Prints commit hash, timestamp, seed, and draft order output
5. **Records the season seed**: Writes the seed to `data/seed.txt`
6. **Commits changes**: Automatically commits the new `data/draft_order.csv` and `data/seed.txt` files

### Seed Generation
The seed is deterministic and generated as follows:
- Takes the first 8 characters of the commit hash
- Converts it to decimal
- Adds the current Unix timestamp
- Because the timestamp is part of it, the seed differs on every run — rerunning the same commit does *not* reproduce the same draft order. What makes a draw reproducible after the fact is the seed being committed to `data/seed.txt`.

### Output
The workflow logs will show:
- Commit Hash
- Runtime Timestamp  
- Generated Seed
- Complete draft order output (position and player for each pick)

### Files Modified
- `data/draft_order.csv` - Updated with new draft order
- `data/seed.txt` - The season seed, reused by the division and schedule draws

### Division and Schedule Draws
These stay out of CI and are run locally after pulling the workflow's commit. They read `data/seed.txt`, so they use the same CI-drawn season seed without it having to be copied out of the workflow logs. Each draw salts the seed differently — see `season_seed.py`. 