# GitHub Actions Workflows

## Draft Order Generation

The `draft-order.yml` workflow automatically generates a new draft order whenever the `data/players.csv` file is modified.

### Trigger Conditions
- Push to `main` or `master` branch that includes changes to `data/players.csv`
- Pull request to `main` or `master` branch that includes changes to `data/players.csv`

### What It Does
1. **Sets up the environment**: Python 3.9 + Poetry with all dependencies
2. **Generates a deterministic seed**: Combines commit hash and runtime timestamp
3. **Runs draft order generation**: Executes `draft_order.py` with the generated seed
4. **Logs all information**: Prints commit hash, timestamp, seed, and draft order output
5. **Commits changes**: Automatically commits the new `data/draft_order.csv` file (only on push events)

### Seed Generation
The seed is deterministic and generated as follows:
- Takes the first 8 characters of the commit hash
- Converts it to decimal
- Adds the current Unix timestamp
- This ensures the same commit will always generate the same draft order

### Output
The workflow logs will show:
- Commit Hash
- Runtime Timestamp  
- Generated Seed
- Complete draft order output (position and player for each pick)

### Files Modified
- `data/draft_order.csv` - Updated with new draft order 