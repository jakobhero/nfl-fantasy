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
    base_seed, draw_seed = resolve_seed('draft_order', args.seed)
    print(f'Season seed: {base_seed} (draft order draw seed: {draw_seed})')
    random.seed(draw_seed)

    #determine draft order and write to data/draft_order.csv
    players_df = pd.read_csv('data/players.csv')
    players_list = list(players_df['player'])
    order = [(pos+1, player) for pos, player in enumerate(random.sample(players_list, len(players_list)))]
    order_df = pd.DataFrame(order, columns=['position', 'player'])
    for pick in order_df.to_dict(orient='records'):
        print(f'Pick #{pick["position"]}: {pick["player"]}') 
    order_df.to_csv('data/draft_order.csv', index=False)
