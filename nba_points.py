from nba_api.stats.endpoints import PlayerGameLogs
import pandas as pd
import math

def rename_columns(df: pd.DataFrame):
    df.columns = list(map("_".join, df.columns.values))
    new_cols_dict = {col:col[:len(col.split("_")[0])] for col in df.columns}
    df.rename(columns=new_cols_dict, inplace=True)


player_game_logs = PlayerGameLogs(
    season_nullable="2024-25",
    season_type_nullable="Regular Season"
)

df_nba = player_game_logs.get_data_frames()[0]

df = df_nba\
    .groupby(["TEAM_ABBREVIATION", "TEAM_NAME", "GAME_ID"])\
    .agg({
        "FTM" : ["sum"],
        "FGM" : ["sum"],
        "FG3M" : ["sum"]
    })

rename_columns(df)

df["FG2M"] = df["FGM"] - df["FG3M"]

df.reset_index(inplace=True)


df = df\
    .groupby(["TEAM_ABBREVIATION", "TEAM_NAME"])\
    .agg(
        {
            "GAME_ID" : ["count"],
            "FTM" : ["mean"],
            "FGM" : ["mean"],
            "FG3M" : ["mean"],
            "FG2M" : ["mean"]

        }
    )

rename_columns(df)

# df[["FTM", "FGM", "FG3M", "FG2M"]] = df[["FTM", "FGM", "FG3M", "FG2M"]].apply(lambda x: math.floor(x))
df[["FTM", "FGM", "FG3M", "FG2M"]] = df[["FTM", "FGM", "FG3M", "FG2M"]].astype(int)

df.to_csv("nba_field_goals.csv")