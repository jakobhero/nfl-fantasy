import random
import pandas as pd
import argparse

from season_seed import is_drawn, read_season, record_season_seed, resolve_seed, season_path

if __name__ == '__main__':
    #read seed value from command line argument, defaults to the recorded season seed
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--force', action='store_true',
                        help='redraw a season that has already been drawn')
    args = parser.parse_args()

    #a drawn season is final: everyone has seen the order, so redrawing it has to be
    #a deliberate act rather than a side effect of rerunning the workflow
    season = read_season()
    if is_drawn() and not args.force:
        raise SystemExit(
            f'The {season} season has already been drawn, see {season_path("draft_order.csv")}. '
            'Bump data/season.txt for a new season, or pass --force to redraw this one.'
        )

    #configure seed
    base_seed, draw_seed = resolve_seed('draft_order', args.seed)
    print(f'Season {season} | seed: {base_seed} (draft order draw seed: {draw_seed})')
    random.seed(draw_seed)

    #determine draft order and write it next to the seed it was drawn from
    players_df = pd.read_csv('data/players.csv')
    players_list = list(players_df['player'])
    order = [(pos+1, player) for pos, player in enumerate(random.sample(players_list, len(players_list)))]
    order_df = pd.DataFrame(order, columns=['position', 'player'])
    for pick in order_df.to_dict(orient='records'):
        print(f'Pick #{pick["position"]}: {pick["player"]}')
    record_season_seed(base_seed)
    order_df.to_csv(season_path('draft_order.csv'), index=False)
