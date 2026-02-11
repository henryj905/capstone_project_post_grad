import nfl_data_py as nfl
import os
import pandas as pd

def player_list(year):
    print("Getting info")

    depth_charts = nfl.import_depth_charts([year])

    players = depth_charts[["gsis_id", "full_name", "club_code", "position", "depth_team"]]
    print("Data received")
    return players.drop_duplicates()

def team_schedule(year):
    data = nfl.import_schedules([year])
    teams = data[["away_team"]].drop_duplicates().sort_values("away_team").reset_index(drop =True)
    teams.index = teams.index+1
    print(teams)
    selection = input("Select team to view schedule: \n")
    selection = selection.upper()

    games = data[
        (data["home_team"] == selection) | (data["away_team"] == selection)
        ].copy()

    games["location"] = games.apply(lambda row: "HOME" if row["home_team"] == selection else "AWAY", axis =1)
    games = games.reset_index(drop = True)
    games.index = games.index +1

    schedule = games[["week", "away_team", "home_team", "location"]].to_string(index=False)
    return schedule

def passing_yards_in_season(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id","player_name", "recent_team", "position"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    passing_yards = seasonal_with_names[seasonal_with_names["passing_yards"] > 0]
    return passing_yards[["player_name","recent_team","position", "passing_yards"]].sort_values("recent_team")

def rushing_stats(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team", "position"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    rushing_yards = seasonal_with_names[seasonal_with_names["rushing_yards"] > 0]
    rushing_yards = rushing_yards[["player_name", "recent_team", "position", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles","rushing_fumbles_lost"]]
    return rushing_yards.to_string(index=False)

def attempts_completions(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([2024])
    weekly = nfl.import_weekly_data([2024], columns=["player_id", "player_name"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    percentage = seasonal_with_names[seasonal_with_names["attempts"] > 0]
    percentage = percentage[["player_name", "completions", "attempts"]]
    percentage["completion_pct"] = (percentage["completions"] / percentage["attempts"] * 100).round(2)
    percentage = percentage.sort_values("attempts")
    return percentage

def TD_INT_ratio(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    TDI = seasonal_with_names[seasonal_with_names["passing_tds"] > 0]
    TDI = TDI[["player_name", "passing_tds", "interceptions"]]

    TDI["ratio"] = (TDI["passing_tds"] / TDI["interceptions"]).round(2)
    TDI.loc[TDI["interceptions"] == 0, "ratio"] = "NO INT"
    TDI = TDI.sort_values("passing_tds")
    return TDI

def receiving_stats(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    seasonal_data = nfl.import_seasonal_data([2024])
    weekly = nfl.import_weekly_data([2024], columns=["player_id", "player_name"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    YAC = seasonal_with_names[seasonal_with_names["targets"] > 0]
    YAC = YAC[
        ["player_name", "receptions", "targets", "receiving_yards", "receiving_yards_after_catch", "receiving_tds"]]

    YAC["rec_to_tar"] = (YAC["receptions"] / YAC["targets"]).round(2)
    YAC["rec_to_yards"] = (YAC["receptions"] / YAC["receiving_yards"]).round(2)
    YAC = YAC.sort_values("targets")
    return YAC.to_string(index = False)

def special_teams_tds(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([2024])
    weekly = nfl.import_weekly_data([2024], columns=["player_id", "player_name", "recent_team"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    total = seasonal_with_names[seasonal_with_names["special_teams_tds"] > 0]
    total = total[["player_id", "player_name", "recent_team", "special_teams_tds"]].sort_values("recent_team")
    return total

def sacks_by_qb(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    seasonal_data = nfl.import_seasonal_data([2024])
    weekly = nfl.import_weekly_data([2024], columns=["player_id", "player_name", "recent_team"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    sacks = seasonal_with_names[seasonal_with_names["sacks"] > 0]
    sacks = sacks[["player_id", "player_name", "recent_team", "sacks", "sack_yards", "sack_fumbles", "sack_fumbles_lost"]].sort_values(
        "sacks")
    return sacks.to_string(index = False)

if __name__ == "__main__":
    user_input = input("select option").upper()
    year = int(input("Enter season (2017-2024):\n"))
    if user_input == "PLAYERS":
        players = player_list(year)
        if os.path.exists('nfl_players.xlsx'):
            os.remove('nfl_players.xlsx')
        players.to_excel('nfl_players.xlsx', index=False)
    elif user_input == "SCHEDULES":
        print(team_schedule(year))
    elif user_input == "PASSING YARDS":
        print(passing_yards_in_season(year))
    elif user_input =="RUSHING STATS":
        print(rushing_stats(year))
    elif user_input == "COMPLETION PERCENTAGE":
        print(attempts_completions(year))
    elif user_input == "TD INT RATIO":
        print(TD_INT_ratio(year))
    elif user_input == "RECEIVING STATS":
        print(receiving_stats(year))
    elif user_input == "SPECIAL TEAMS":
        print(special_teams_tds(year))
    elif user_input == "SACKS":
        print(sacks_by_qb(year))
    else:
        print("Invalid input. Please select from options or QUIT.")
