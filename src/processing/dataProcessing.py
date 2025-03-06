"""
    Data Processing and Injection for NBA Stats Project
    @fjorge

"""

# Importing
import pandas as pd
import logging
import sqlite3

# Setup logger
logger = logging.getLogger("processing")
logging.basicConfig()

############################################################

# MAIN DATA PRCOESSING LOGIC
def process_data(ingest_data):

    logger.info("Processing function triggered")

    # Extract player data
    player_df = pd.DataFrame(
        data=ingest_data["player_data"]["rowSet"], 
        columns=ingest_data["player_data"]["headers"]
        )
    
    # Process
    player_df["FIRST_NAME"] = player_df["DISPLAY_FIRST_LAST"].apply(lambda x: str(x).split(" ")[0])
    player_df["LAST_NAME"] = player_df["DISPLAY_FIRST_LAST"].apply(lambda x: str(x).split(" ")[1])

    # Choose data fields
    cols = ["PERSON_ID", "FIRST_NAME", "LAST_NAME", "TEAM_ID"]
    proc_player_df = player_df[cols]

    # Extract player stats
    player_id_list = ingest_data["player_stats"].keys()
    player_stats = []
    for player_id in player_id_list:
        try: 
            player_stat_data = ingest_data["player_stats"][player_id]["rowSet"][0]
            player_stats.append(player_stat_data)
        except:
            print("No data from player {}".format(player_id))
            continue
    player_stat_df = pd.DataFrame(
        data=player_stats, 
        columns = ['PERSON_ID', 'LEAGUE_ID', 'TEAM_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    )
    # Choose data fields
    cols = ['PERSON_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    proc_player_stat_df = player_stat_df[cols]

    proc_player_stat_df.to_csv("test.csv")

    # Merge data frames
    proc_data = pd.merge(proc_player_df, proc_player_stat_df, on="PERSON_ID", how="outer")

    # Ensure data types and handle NaNs
    proc_data["PERSON_ID"] = proc_data["PERSON_ID"].astype(int)
    proc_data["FIRST_NAME"] = proc_data["FIRST_NAME"].astype(str)
    proc_data["LAST_NAME"] = proc_data["LAST_NAME"].astype(str)
    proc_data["TEAM_ID"] = proc_data["TEAM_ID"].astype(int)
    proc_data["GP"] = proc_data["GP"].fillna(-1).astype(int)
    proc_data["GS"] = proc_data["GS"].fillna(-1).astype(int)
    proc_data["MIN"] = proc_data["MIN"].fillna(-1).astype(float)
    proc_data["FGM"] = proc_data["FGM"].fillna(-1).astype(int)
    proc_data["FGA"] = proc_data["FGA"].fillna(-1).astype(int)
    proc_data["FG_PCT"] = proc_data["FG_PCT"].fillna(-1).astype(float)
    proc_data["FG3M"] = proc_data["FG3M"].fillna(-1).astype(int)
    proc_data["FG3A"] = proc_data["FG3A"].fillna(-1).astype(int)
    proc_data["FG3_PCT"] = proc_data["FG3_PCT"].fillna(-1).astype(float)
    proc_data["FTM"] = proc_data["FTM"].fillna(-1).astype(int)
    proc_data["FTA"] = proc_data["FTA"].fillna(-1).astype(int)
    proc_data["FT_PCT"] = proc_data["FT_PCT"].fillna(-1).astype(float)
    proc_data["OREB"] = proc_data["OREB"].fillna(-1).astype(int)
    proc_data["DREB"] = proc_data["DREB"].fillna(-1).astype(int)
    proc_data["REB"] = proc_data["REB"].fillna(-1).astype(int)
    proc_data["AST"] = proc_data["AST"].fillna(-1).astype(int)
    proc_data["STL"] = proc_data["STL"].fillna(-1).astype(int)
    proc_data["BLK"] = proc_data["BLK"].fillna(-1).astype(int)
    proc_data["TOV"] = proc_data["TOV"].fillna(-1).astype(int)
    proc_data["PF"] = proc_data["PF"].fillna(-1).astype(int)
    proc_data["PTS"] = proc_data["PTS"].fillna(-1).astype(int)

    # Connect to DB
    conn = sqlite3.connect("db/sqlite-db")
    cursor = conn.cursor()

    # Generate qury
    columns = proc_data.columns.tolist()
    placeholders = ', '.join(['?' for _ in columns])
    update_clause = ', '.join([f"{col} = excluded.{col}" for col in columns if col != "PERSON_ID"])
    insert_update_query = f'''
        INSERT INTO 'playerstats' ({', '.join(columns)}) 
        VALUES ({placeholders})
        ON CONFLICT(PERSON_ID) DO UPDATE SET {update_clause}
    '''
    data_tuples = [tuple(row) for row in proc_data.itertuples(index=False, name=None)]

    # Execute query for each row
    cursor.executemany(insert_update_query, data_tuples)
    
    # Commit changes
    conn.commit()
    conn.close()

    print("Data updated successfully!")

if "__main__" == __name__:
    ingest_data = {}
    output_data = process_data(ingest_data)
