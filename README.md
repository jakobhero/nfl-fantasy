# NFL Fantasy
This Repository contains scripts to draw draft order, divisions, and schedule for NFL fantasy.
## Getting Started
This project was implemented in a dev environment inside a dev container. To reproduce the dev environment, follow these steps:
1. Prerequisites are a Docker daemon and VS Code
2. Install the devcontainer extension from the VS Code marketplace and then select Dev Containers: Reopen in Container in the command palette with this repository open.
## Preparing a New Season
1. Update `data/players.csv` with this season's roster. Make sure the roster size is **even** and **divisible by the number of divisions** in `data/divisions.csv` — adjust `data/divisions.csv` if it is not. Both draws refuse to run otherwise.
2. Push the change to `main`. The draft order workflow draws the season seed, writes the draft order to `data/draft_order.csv` and the seed to `data/seed.txt`, and commits both.
3. Pull, then run the division and schedule draws locally. They pick up `data/seed.txt` automatically, so no seed needs to be passed:
   ```
   python division_draw.py
   python schedule_draw.py
   ```
4. Commit `data/division_mapping.csv` and `data/schedule.csv` if you want the season on record.

### The Season Seed
All three draws run off one season seed, drawn in CI so nobody can pick a favourable one, and recorded in `data/seed.txt` so every draw can be reproduced later. Each draw salts that seed differently (see `season_seed.py`): seeding two `random.sample` calls with the same value over equally sized populations replays the same permutation, which would tie a player's draft position to their division. Passing `--seed` explicitly overrides the recorded seed for any script.

## Functionalities
The following functionalities are implemented:
### Determine Draft Order
In order to determine the draft order, run `python draft_order.py`. The script reads the players provided in `data/players.csv` and writes the resulting order to `data/draft_order.csv`. You can specify the seed by passing it as named argument, e.g. `python draft_order.py --seed 25` to set the seed value to 25; otherwise the season seed in `data/seed.txt` is used.
### Assign Divisions
In order to assign divisions, run `python division_draw.py`. The script reads the players and division names provided in the respective `.csv`s in `/data` and writes the resulting mapping of players to divisions to `data/division_mapping.csv`. The roster has to divide evenly into the divisions, otherwise the script exits with an error. You can specify the seed by passing it as named argument, e.g. `python division_draw.py --seed 25` to set the seed value to 25; otherwise the season seed in `data/seed.txt` is used.
### Create Schedule
In order to create a schedule, run `python schedule_draw.py`. The script reads the assignment of players to divisions in `data/division_mapping.csv` and writes a schedule to `data/schedule.csv`. The roster has to be even, otherwise the script exits with an error. You can specify the seed by passing it as named argument, e.g. `python schedule_draw.py --seed 25` to set the seed value to 25; otherwise the season seed in `data/seed.txt` is used.
 