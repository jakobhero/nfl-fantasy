import random
import pandas as pd
import argparse

from season_seed import resolve_seed

if __name__ == '__main__':
    #read seed value from command line argument, defaults to the committed season seed
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()

    #configure seed
    base_seed, draw_seed = resolve_seed('divisions', args.seed)
    print(f'Season seed: {base_seed} (divisions draw seed: {draw_seed})')
    random.seed(draw_seed)

    #determine player - division mapping and write to data/division_mapping.csv
    divisions_df = pd.read_csv('data/divisions.csv')
    divisions_list = list(divisions_df['division'])
    players_df = pd.read_csv('data/players.csv')
    players_list = list(players_df['player'])

    #every division has to end up the same size, otherwise the lot is shorter than the
    #roster and zip() would silently drop the players that did not fit
    if len(players_list) % len(divisions_list) != 0:
        raise SystemExit(
            f'Cannot draw divisions: {len(players_list)} players do not split evenly into '
            f'{len(divisions_list)} divisions. Adjust data/players.csv or data/divisions.csv.'
        )

    division_lot = divisions_list * int(len(players_list) / len(divisions_list))
    division_lot_assigned = random.sample(division_lot, len(division_lot))
    division_mapping_df = pd.DataFrame(zip(players_list, division_lot_assigned), columns=['player', 'division'])
    division_mapping_df.to_csv('data/division_mapping.csv', index=False)
