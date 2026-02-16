import nfl_data_py as nfl
import os
import OffensiveStats
import pandas as pd


def player_list(year):
    depth_charts = nfl.import_depth_charts([year])
    players = depth_charts[["gsis_id", "full_name", "club_code", "position", "depth_team"]]
    return players.drop_duplicates()


def team_schedule(year):
    data = nfl.import_schedules([year])
    teams = data[["away_team"]].drop_duplicates().sort_values("away_team")
    teams = teams.reset_index(drop=True)
    teams.index += 1
    print(teams)
    selection = input("Select team to view schedule: \n")
    selection = selection.upper()

    games = data[(data["home_team"] == selection) | (data["away_team"] == selection)].copy()

    games["location"] = games.apply(lambda row: "HOME" if row["home_team"] == selection else "AWAY", axis=1)
    games = games.reset_index(drop=True)
    games.index = games.index+1

    schedule = games[["week", "away_team", "home_team", "location"]].to_string(index=False)
    return schedule


def special_teams_tds(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    total = seasonal_with_names[seasonal_with_names["special_teams_tds"] > 0]
    total = total[["player_id", "player_name", "recent_team", "special_teams_tds"]].sort_values("recent_team")
    return total


if __name__ == "__main__":
    user_input = input("select option").upper()
    user_year = int(input("Enter season (2017-2024):\n"))

    if user_input == "PLAYERS":
        if os.path.exists('nfl_players.xlsx'):
            os.remove('nfl_players.xlsx')
        player_list(user_year).to_excel('nfl_players.xlsx', index=False)

    elif user_input == "SCHEDULES":
        print(team_schedule(user_year))
    elif user_input == "PASSING STATS":
        print(OffensiveStats.passing_stats(user_year))

    elif user_input == "RUSHING STATS":
        print(OffensiveStats.rushing_stats(user_year))

    elif user_input == "RECEIVING STATS":
        print(OffensiveStats.receiving_stats(user_year))

    elif user_input == "SPECIAL TEAMS":
        print(special_teams_tds(user_year))

    elif user_input == "SACKS":
        print(OffensiveStats.sacks_by_qb(user_year))

    else:
        print("Invalid input. Please select from options or QUIT.")
