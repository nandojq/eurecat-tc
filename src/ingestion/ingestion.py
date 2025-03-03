"""
    Data Ingestion for NBA Stats Project
    @fjorge

"""

# Importing
import requests
from requests import HTTPError, Timeout, RequestException
from jsonschema import validate, ValidationError
import time
# import json
import logging
# from tqdm import tqdm

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
        logger.error("HTTP error occurred: {}".format(http_err))
    except ConnectionError:
        logger.error("Error: Failed to connect to the server")
    except Timeout:
        logger.error("Error: The request timed out")
    except RequestException as req_err:
        logger.error("Error: {}".format(req_err))

############################################################

# MAIN INGESTION LOGIC
def trigger_ingestion():

    logger.info("Ingestion function triggered")

    ## Fetch player data
    logger.debug("Fetching player data...")
    player_data = fetch_data(player_data_url, params=player_data_params)
    player_data = player_data["resultSets"][0]
    logger.debug("Player data successfuly ingested")

    ## Get updated list of player IDs
    player_id_list = [row[0] for row in player_data["rowSet"]]
    # print(player_id_list)

    ## Fetch stat data for each player
    logger.debug("Fetching player stat data...")
    player_stat_dict = {}
    for player_id in player_id_list[0:5]:
        player_stats_params["PlayerID"] = str(player_id)
        data = fetch_data(player_stats_url, params=player_stats_params)
        # Get only career total stats for regular season
        reg_season_stats = next((item for item in data["resultSets"] if item["name"] == "CareerTotalsRegularSeason"), None)
        player_stat_dict[str(player_id)] = reg_season_stats
        time.sleep(0.5)
    logger.debug("Player stat data successfully ingested")

    ## Append player stat data to player data
    logger.debug("Merging ingested data")
    ingest_data = {
        "player_data": player_data,
        "player_stats": player_stat_dict
    }
    logger.info("Ingestion successfully completed")

    return ingest_data

if "__main__" == __name__:
    output_data = trigger_ingestion()
    # print(output_data)
