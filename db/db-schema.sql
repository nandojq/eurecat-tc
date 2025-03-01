CREATE TABLE players (
    PERSON_ID INT PRIMARY KEY,                      -- Player ID
    FIRST_NAME VARCHAR(50) NOT NULL,               -- Player's First Name
    LAST_NAME VARCHAR(50) NOT NULL,                -- Player's Last Name
    TEAM_ID INT,                                    -- Player's Team ID
    GP INT,                                         -- Games Played
    GS INT,                                         -- Games Started
    MIN FLOAT,                                      -- Minutes Played
    FGM INT,                                        -- Field Goals Made
    FGA INT,                                        -- Field Goals Attempted
    FG_PCT FLOAT,                                   -- Field Goal Percentage
    FG3M INT,                                       -- Three-Point Field Goals Made
    FG3A INT,                                       -- Three-Point Field Goals Attempted
    FG3_PCT FLOAT,                                  -- Three-Point Field Goal Percentage
    FTM INT,                                        -- Free Throws Made
    FTA INT,                                        -- Free Throws Attempted
    FT_PCT FLOAT,                                   -- Free Throw Percentage
    OREB INT,                                       -- Offensive Rebounds
    DREB INT,                                       -- Defensive Rebounds
    REB INT,                                        -- Total Rebounds
    AST INT,                                        -- Assists
    STL INT,                                        -- Steals
    BLK INT,                                        -- Blocks
    TOV INT,                                        -- Turnovers
    PF INT,                                         -- Personal Fouls
    PTS INT                                         -- Points
);
