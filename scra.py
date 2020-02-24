"""
scra.py

Script scrapes XFL play-by-play data from their website,
and formats it into an identical form as nflscrapR does for
NFL data. For use by hobbyists wishing to do statistical
analysis on XFL data.

@author Paul Lambert <paul dot lambert at linux dot com>

"""
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

import json
import pandas as pd

def calculate_num_games():
    """
    TODO Actually make this robust. Just worried about getting the
    data processing working for now.
    """
    return 12

def fetch_pbp(url):
    """
    Attempts to get the content at `url' by making an HTTP GET request.
    If the content-type of response is valid, process and return it as JSON; 
    otherwise return None.
    """

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                resp = resp.text

                # our JSON PBP data is stored in a JavaScript var playList
                start = resp.find('playList = ') + len('playList = ')
                end = resp.find('</script>', start)

                # substring and clean the JSON before returning
                pbp = resp[start:end]
                pbp = pbp.strip()
                pbp = pbp[:-1] # remove trailing semicolon from the JS

                return json.loads(pbp)
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1} ' . format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def format_json_for_csv(json_data):
    """
    Attempts to mimic the format used by the very popular package
    for providing NFL CSVs, nflscrapR. 

    Converts the play by play data from scraped JSON into CSV
    
    See https://github.com/maksimhorowitz/nflscrapR for more information
    """

    # print("Match is ", json_data['awayClubCode'] ," @ ", json_data['homeClubCode'])
    # for play in json_data["plays"]:
    #     print(play['PlayDescription'])

    """
    the columns used by xflscrapR (very similar to nflscrapR w/o EPA):

    game, play_id, qtr, time, posteam, Situation, desc
    DriveTime, AwayScoreAfterDrive, HomeScoreAfterDrive,
    home_team, away_team, defteam, Week, game_id,
    quarter_seconds_remaining, half_seconds,remaining,
    game_seconds_remaining, down, ydstogo, yardline_100,
    goal_to_go, play_type, shotgun, no_huddle, qb_spike,
    qb_kneel, sack, qb_scramble, pass_attempt, interception,
    complete_pass, throwaway, pass_length, pass_location,
    run_direction, run_location, run_gap, touchdown, fumble,
    yards_gained, first_down, turnover, turnover_type,
    fumble_lost, fourth_down_decision, extra_point_type,
    extra_point_conversion, penalty, solo_tackle, assist_tackle,
    tackle_for_loss, passer_player_name, receiver_player_name,
    rusher_player_name, interception_player_name, solo_tackle_player_name,
    assist_tackle_1_player_name, assist_tackle_2_player_name
    """
    
    df = pd.json_normalize(json_data["plays"])
    df.to_csv("play_by_play_data/pbp_2020.csv", mode='a', header=True)
    # return json_data

def main():
    num_games = calculate_num_games()

    for match in range(1, num_games+1):
        #print("We're getting the data for Match %d" % (match))
        url = "https://stats.xfl.com/" + str(match)
        json_data = fetch_pbp(url)

        if json_data["plays"] == []:
            print("game hasn't yet been played")
            break
        
        # print(json_data)
        csv_data = format_json_for_csv(json_data)

if __name__ == '__main__':
    main()
    
