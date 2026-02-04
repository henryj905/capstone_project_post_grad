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

def rushing_yards_in_season(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team", "position"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    rushing_yards = seasonal_with_names[seasonal_with_names["rushing_yards"] > 0]
    rushing_yards = rushing_yards[["player_name", "recent_team", "position", "rushing_yards"]]
    return rushing_yards

if __name__ == "__main__":
    user_input = input("select option: \nPlayers\nSchedules\nQuit\nPassing Yards\nRushing Yards\n\n").upper()

    if user_input == "PLAYERS":
        year = int(input("Enter season (2017-2024):\n"))
        players = player_list(year)

        if os.path.exists('nfl_players.xlsx'):
            os.remove('nfl_players.xlsx')
            print(f"{'nfl_players.xlsx'} existed and was deleted.")
        else:
            print(f"{'nfl_players.xlsx'} does not exist, creating new file.")

        players.to_excel('nfl_players.xlsx', index=False)
        print("File saved.")

        print("done")
    elif user_input == "SCHEDULES":
        year = int(input("Enter season (2017-2024):\n"))
        schedules = team_schedule(year)
        print(schedules)
        print("Schedule loaded")
    elif user_input == "PASSING YARDS":
        year = int(input("Enter season (2017-2024):\n"))
        passing = passing_yards_in_season(year)
        sort_by = input("Sort list by: \nName\nTeam\nPosition\nYards\n\n").upper()
        if sort_by == "NAME":
            print(passing.sort_values("player_name"))
        elif sort_by == "TEAM":
            print(passing.sort_values("recent_team"))
        elif sort_by == "POSITION":
            print(passing.sort_values("position"))
        elif sort_by == "YARDS":
            print(passing.sort_values("passing_yards"))
        print("Passing Yards Shown\n")
    elif user_input =="RUSHING YARDS":
        year = int(input("Enter season (2017-2024):\n"))
        rushing = rushing_yards_in_season(year)
        sort_by = input("Sort list by: \nName\nTeam\nPosition\nYards\n\n").upper()
        if sort_by == "NAME":
            print(rushing.sort_values("player_name"))
        elif sort_by == "TEAM":
            print(rushing.sort_values("recent_team"))
        elif sort_by == "POSITION":
            print(rushing.sort_values("position"))
        elif sort_by == "YARDS":
            print(rushing.sort_values("rushing_yards"))
        print("Rushing Yards Shown")
    else:
        print("Invalid input. Please type PLAYERS, SCHEDULES, PASSING YARDS, RUSHING YARDS, or QUIT.")
