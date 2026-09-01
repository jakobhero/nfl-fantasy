# NFL Fantasy
This Repository contains scripts to draw draft order, divisions, and schedule for NFL fantasy.
## Getting Started
The project is managed with [uv](https://docs.astral.sh/uv/) and runs on the Python version pinned in `.python-version`. With uv installed, `uv sync` provisions that Python and the locked dependencies — no separate Python install needed:
```
uv sync
uv run python draft_order.py
```
Prefix each script with `uv run` and it executes against the locked environment.

Alternatively the project can be worked on inside a dev container:
1. Prerequisites are a Docker daemon and VS Code
2. Install the devcontainer extension from the VS Code marketplace and then select Dev Containers: Reopen in Container in the command palette with this repository open.
## Preparing a New Season
1. Set `data/season.txt` to the new season, e.g. `2026`. Every draw for that season is written to `data/<season>/`, so a new season can never overwrite a past one.
2. Update `data/players.csv` with this season's roster. Make sure the roster size is **even** and **divisible by the number of divisions** in `data/divisions.csv` — adjust `data/divisions.csv` if it is not. Both draws refuse to run otherwise.
3. Open a pull request with those changes and add the **`draw-order`** label to it. Merging a labelled pull request runs the draw, which writes `data/<season>/draft_order.csv` and `data/<season>/seed.txt` and commits them. Editing the roster without that label never redraws anything.
4. Pull, then run the division and schedule draws locally. They pick up the season seed automatically, so no seed needs to be passed:
   ```
   uv run python division_draw.py
   uv run python schedule_draw.py
   ```
5. Commit `data/<season>/division_mapping.csv` and `data/<season>/schedule.csv`.

A season that has already been drawn is final: the draft order draw refuses to overwrite it. Bump `data/season.txt` for a new season, or pass `--force` to deliberately redraw the current one.

### The Season Seed
All three draws run off one season seed, drawn in CI so nobody can pick a favourable one, and recorded in `data/<season>/seed.txt` so every draw can be reproduced later. Each draw salts that seed differently (see `season_seed.py`): seeding two `random.sample` calls with the same value over equally sized populations replays the same permutation, which would tie a player's draft position to their division. Passing `--seed` explicitly overrides the recorded seed for any script.

## Functionalities
The following functionalities are implemented:
### Determine Draft Order
In order to determine the draft order, run `uv run python draft_order.py`. The script reads the players provided in `data/players.csv` and writes the resulting order to `data/<season>/draft_order.csv`. You can specify the seed by passing it as named argument, e.g. `uv run python draft_order.py --seed 25` to set the seed value to 25; otherwise the recorded season seed is used.
### Assign Divisions
In order to assign divisions, run `uv run python division_draw.py`. The script reads the players and division names provided in the respective `.csv`s in `/data` and writes the resulting mapping of players to divisions to `data/<season>/division_mapping.csv`. The roster has to divide evenly into the divisions, otherwise the script exits with an error. You can specify the seed by passing it as named argument, e.g. `uv run python division_draw.py --seed 25` to set the seed value to 25; otherwise the recorded season seed is used.
### Create Schedule
In order to create a schedule, run `uv run python schedule_draw.py`. The script reads the assignment of players to divisions in `data/<season>/division_mapping.csv` and writes a schedule to `data/<season>/schedule.csv`. The roster has to be even, otherwise the script exits with an error. You can specify the seed by passing it as named argument, e.g. `uv run python schedule_draw.py --seed 25` to set the seed value to 25; otherwise the recorded season seed is used.
 