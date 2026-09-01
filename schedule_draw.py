import random
import pandas as pd
import argparse
import time

from season_seed import resolve_seed

def assign_pairings_to_weeks(assignable_weeks, players_list, pairings, seed):
    random.seed(seed)
    attempt = 1
    while True:
        try: 
            schedule = []
            pairings_drawn = random.sample(pairings, len(pairings))
            for week in assignable_weeks:
                players_drawable = players_list.copy()
                pairings_counter, week_fully_drawn = 0, False
                while week_fully_drawn == False:
                    pairing = pairings_drawn[pairings_counter]
                    if pairing[0] in players_drawable and pairing[1] in players_drawable:
                        schedule.append((week, pairings_drawn.pop(pairings_counter)))
                        players_drawable.remove(pairing[0])
                        players_drawable.remove(pairing[1])
                        parings_counter = 0
                    else:
                        pairings_counter += 1
                    if len(players_drawable) == 0:
                        week_fully_drawn = True
            return schedule
        except:
            attempt += 1
            seed += 1
            random.seed(seed)
            continue

if __name__ == '__main__':
    #read seed value from command line argument, defaults to the committed season seed
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()

    base_seed, draw_seed = resolve_seed('schedule', args.seed)
    print(f'Season seed: {base_seed} (schedule draw seed: {draw_seed})')

    division_mapping_df = pd.read_csv('data/division_mapping.csv')
    players_list = list(division_mapping_df.player)
    division_count = len(division_mapping_df.division.unique())

    #every player is paired up every week, so an odd roster can never fill a week and
    #assign_pairings_to_weeks would keep retrying with new seeds forever
    if len(players_list) % 2 != 0:
        raise SystemExit(
            f'Cannot draw a schedule: {len(players_list)} players cannot be paired up evenly. '
            'Adjust data/players.csv and rerun the division draw.'
        )

    full_schedule = []

    #create first part of schedule
    pairings = [(players_list[i], players_list[j]) for i in range(len(players_list)) for j in range(i + 1, len(players_list))]
    schedule_first_part = assign_pairings_to_weeks(range(1, len(players_list)), players_list, pairings, draw_seed)
    full_schedule += schedule_first_part
    
    #create second part of schedule
    division_dict ={row.player: row.division for row in division_mapping_df.itertuples()}
    week_range = range(len(players_list), len(players_list) + int(len(players_list) / division_count - 1))
    pairings = [(players_list[i], players_list[j]) for i in range(len(players_list)) for j in range(i + 1, len(players_list)) if division_dict[players_list[i]] == division_dict[players_list[j]]]
    schedule_second_part = assign_pairings_to_weeks(week_range, players_list, pairings, draw_seed)
    full_schedule += schedule_second_part
    
    schedule_df = pd.DataFrame(full_schedule, columns = ['week', 'pairing'])
    schedule_df.to_csv('data/schedule.csv', index=False)
    