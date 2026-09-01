import os

SEASON_FILE = 'data/season.txt'

#each draw gets its own salt: seeding two random.sample calls with the same value
#over equally sized populations replays the same permutation, which would tie a
#player's draft position to their division instead of drawing them independently
SALTS = {
    'draft_order': 0,
    'divisions': 1000003,
    'schedule': 2000003,
}


def read_season():
    if not os.path.exists(SEASON_FILE):
        raise SystemExit(f'No season found at {SEASON_FILE}. It should hold a single year, e.g. 2026.')
    with open(SEASON_FILE) as f:
        season = f.read().strip()
    if not season:
        raise SystemExit(f'{SEASON_FILE} is empty. It should hold a single year, e.g. 2026.')
    return season


def season_dir():
    #every season keeps its own draws, so a new one can never overwrite a past one
    return os.path.join('data', read_season())


def season_path(filename):
    return os.path.join(season_dir(), filename)


def is_drawn():
    return os.path.exists(season_path('seed.txt'))


def read_season_seed():
    #the season seed is recorded by the draft order draw, see .github/workflows/draft-order.yml
    path = season_path('seed.txt')
    if not os.path.exists(path):
        raise SystemExit(
            f'The {read_season()} season has not been drawn yet, so there is no seed at {path}. '
            'Run the draft order draw first, or pass a seed explicitly with --seed.'
        )
    with open(path) as f:
        return int(f.read().strip())


def record_season_seed(seed):
    os.makedirs(season_dir(), exist_ok=True)
    with open(season_path('seed.txt'), 'w') as f:
        f.write(f'{seed}\n')


def resolve_seed(draw, seed=None):
    #fall back to the recorded season seed when no seed was passed on the command line
    base_seed = read_season_seed() if seed is None else seed
    return base_seed, base_seed + SALTS[draw]
