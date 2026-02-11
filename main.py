import nfl_data_py as nfl
import os
import OffensiveStats
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
        print(OffensiveStats.passing_yards_in_season(year))
    elif user_input =="RUSHING STATS":
        print(OffensiveStats.rushing_stats(year))
    elif user_input == "COMPLETION PERCENTAGE":
        print(OffensiveStats.attempts_completions(year))
    elif user_input == "TD INT RATIO":
        print(OffensiveStats.TD_INT_ratio(year))
    elif user_input == "RECEIVING STATS":
        print(OffensiveStats.receiving_stats(year))
    elif user_input == "SPECIAL TEAMS":
        print(OffensiveStats.special_teams_tds(year))
    elif user_input == "SACKS":
        print(OffensiveStats.sacks_by_qb(year))
    else:
        print("Invalid input. Please select from options or QUIT.")
