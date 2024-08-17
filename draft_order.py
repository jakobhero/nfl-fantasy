import random
import pandas as pd
import argparse

if __name__ == '__main__':
    #read seed value from command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    
    #configure seed
    random.seed(args.seed)
    
    #determine draft order and write to data/draft_order.csv
    players_df = pd.read_csv('data/players.csv')
    players_list = list(players_df['player'])
    order = [(pos+1, player) for pos, player in enumerate(random.sample(players_list, len(players_list)))]
    order_df = pd.DataFrame(order, columns=['position', 'player'])
    order_df.to_csv('data/draft_order.csv', index=False)
