"""
    Data Ingestion for NBA Stats Project
    @fjorge

"""

# Importing
import requests
from requests import HTTPError, Timeout, RequestException
from jsonschema import validate, ValidationError
import time
import json

from tqdm import tqdm
############################################################

# NBA API Endpoint Data
## Player Data
## https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/commonallplayers.md
player_data_url = "https://stats.gleague.nba.com/stats/commonallplayers/"
player_data_params = {
    "leagueId": "00", 
    "season": "2024-25", 
    "isOnlyCurrentSeason": "1"}
## Player Stat Data
## https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playercareerstats.md
player_stats_url = "https://stats.gleague.nba.com/stats/playercareerstats/"
player_stats_params = {"PerMode": "Totals", "PlayerID": 0, "leagueId": "00"}
############################################################

# API Data Fetch Function
def fetch_data(url, params=None, headers=None, timeout=10):
    """ Generic function to handle data fetch API """
    # Try to fetch data
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()  
        return response.json()
    
    # Error handling
    except HTTPError as http_err:
        print("HTTP error occurred: {}".format(http_err))
    except ConnectionError:
        print("Error: Failed to connect to the server")
    except Timeout:
        print("Error: The request timed out")
    except RequestException as req_err:
        print("Error: {}".format(req_err))

############################################################

# MAIN INGESTION LOGIC

## Fetch player data
player_data = fetch_data(player_data_url, params=player_data_params)
player_data = player_data["resultSets"][0]

## Get updated list of player IDs
player_id_list = [row[0] for row in player_data["rowSet"]]
# print(player_id_list)

## Fetch stat data for each player
player_stat_dict = {}
for player_id in tqdm(player_id_list):
    player_stats_params["PlayerID"] = str(player_id)
    data = fetch_data(player_stats_url, params=player_stats_params)
    # Get only career total stats for regular season
    reg_season_stats = next((item for item in data["resultSets  "] if item["name"] == "CareerTotalsRegularSeason"), None)
    player_stat_dict[str(player_id)] = reg_season_stats
    time.sleep(0.5)

## Append player stat data to player data
ingest_data = {
    "player_data": player_data,
    "player_stats": player_stat_dict
}

## Save to file (debug)
import json
with open("./src/ingestion/ingest_output_example.json", 'w') as json_file:
    json.dump(ingest_data, json_file, indent=4)
