from nba_api.stats.endpoints import PlayerGameLogs
import pandas as pd
import os

# Funció per a reanomenar correctament les columnes calculades
def rename_columns(df: pd.DataFrame):
    df.columns = list(map("_".join, df.columns.values))
    new_cols_dict = {col:col[:len(col.split("_")[0])] for col in df.columns}
    df.rename(columns=new_cols_dict, inplace=True)

# Recopilem i estructurem les dades
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
            "FG3M" : ["mean"],
            "FG2M" : ["mean"]

        }
    )
rename_columns(df)
df.reset_index(inplace=True)
df[["FTM", "FG3M", "FG2M"]] = df[["FTM", "FG3M", "FG2M"]].apply(round, 0).astype(int)
df["PTS"] = df["FTM"] + df["FG2M"] * 2 + df["FG3M"] * 3
df.sort_values(by="PTS", ascending=False, inplace=True)

# Escollim els 3 equips més anotadors i els 3 menys anotadors
df = pd.concat([df.head(5), df.sort_values(by="PTS", ascending=True).head(5)])

df.to_csv("./data/nba_field_goals_scrap.csv")