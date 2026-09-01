import os

SEED_FILE = 'data/seed.txt'

#each draw gets its own salt: seeding two random.sample calls with the same value
#over equally sized populations replays the same permutation, which would tie a
#player's draft position to their division instead of drawing them independently
SALTS = {
    'draft_order': 0,
    'divisions': 1000003,
    'schedule': 2000003,
}


def read_season_seed():
    #the season seed is written by the draft order workflow, see .github/workflows/draft-order.yml
    if not os.path.exists(SEED_FILE):
        raise SystemExit(
            f'No season seed found at {SEED_FILE}. Pass one explicitly with --seed, '
            'or pull the seed the draft order workflow committed.'
        )
    with open(SEED_FILE) as f:
        return int(f.read().strip())


def resolve_seed(draw, seed=None):
    #fall back to the committed season seed when no seed was passed on the command line
    base_seed = read_season_seed() if seed is None else seed
    return base_seed, base_seed + SALTS[draw]
