# NFL Fantasy
This Repository contains scripts to draw draft order, divisions, and schedule for NFL fantasy.
## Getting Started
This project was implemented in a dev environment inside a dev container. To reproduce the dev environment, follow these steps:
1. Prerequisites are a Docker daemon and VS Code
2. Install the devcontainer extension from the VS Code marketplace and then select Dev Containers: Reopen in Container in the command palette with this repository open.
## Functionalities
The following functionalities are implemented:
### Determine Draft Order
In order to determine the draft order, run `python draft_order.py`. The script reads the players provided in `data/players.csv` and writes the resulting order to `data/draft_order.csv`. You can specify the seed by passing it as named argument, e.g. `python draft_order.py --seed 25` to set the seed value to 25.
### Assign Divisions
In order to assign divisions, run `python division_draw.py`. The script reads the players and division names provided in the respective `.csv`s in `/data` and writes the resulting mapping of players to divisions to `data/division_mapping.csv`. You can specify the seed by passing it as named argument, e.g. `python division_draw.py --seed 25` to set the seed value to 25.
### Create Schedule
In order to create a schedule, run `python schedule_draw.py`. The script reads the assignment of players to divisions in `data/division_mapping.csv` and writes a schedule to `data/schedule.csv`. You can specify the seed by passing it as named argument, e.g. `python schedule_draw.py --seed 25` to set the seed value to 25.
 