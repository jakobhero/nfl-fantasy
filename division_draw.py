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
    
    #determine player - division mapping and write to data/division_mapping.csv
    divisions_df = pd.read_csv('data/divisions.csv')
    divisions_list = list(divisions_df['division'])
    players_df = pd.read_csv('data/players.csv')
    players_list = list(players_df['player'])
    division_lot = divisions_list * int(len(players_list) / len(divisions_list))
    division_lot_assigned = random.sample(division_lot, len(division_lot))
    division_mapping_df = pd.DataFrame(zip(players_list, division_lot_assigned), columns=['player', 'division'])
    division_mapping_df.to_csv('data/division_mapping.csv', index=False)
