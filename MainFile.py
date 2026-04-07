import nfl_data_py as nfl
import pandas as pd


def player_list(year):
    depth_charts = nfl.import_depth_charts([year])
    players = depth_charts[["gsis_id", "full_name", "club_code", "position", "depth_team"]]
    return players.drop_duplicates()


def team_schedule(year, team_abbr):
    data = nfl.import_schedules([year])
    teams = data[["away_team"]].drop_duplicates().sort_values("away_team")
    teams = teams.reset_index(drop=True)
    teams.index += 1
    selection = team_abbr.upper()

    games = data[(data["home_team"] == selection) | (data["away_team"] == selection)].copy()

    games["location"] = games.apply(lambda row: "HOME" if row["home_team"] == selection else "AWAY", axis=1)
    games = games.reset_index(drop=True)
    games.index = games.index+1

    schedule = games[["week", "home_team", "away_team", "location"]]
    return schedule


def team_schedule_pick_week(year, team_abbr, week):
    schedule = team_schedule(year, team_abbr)
    schedule = schedule[schedule["week"] == week]
    return schedule


def return_opponent(year, team_abbr, week):
    team_abbr = team_abbr.upper()
    schedule = team_schedule_pick_week(year, team_abbr, week)
    opponent = ''

    if schedule.empty:
        opponent = "BYE"
        return opponent
    for _, row, in schedule.iterrows():
        if row["home_team"] == team_abbr:
            opponent = row["away_team"]
        elif row["away_team"] == team_abbr:
            opponent = row["home_team"]
    return opponent


def depth_chart(year, team_abbr, week_num):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    data = nfl.import_weekly_rosters([year])

    data = data[["week", "player_id", "player_name", "team", "depth_chart_position", "status"]]
    team_abbr = team_abbr.upper()
    data = data[data["team"] == team_abbr]
    data = data[data["week"] == week_num]

    return data.sort_values(["week", "team", "depth_chart_position"])


def teams():
    abbr = nfl.import_team_desc()
    abbr = abbr[["team_abbr", "team_name"]]

    teams_to_remove = ["LAR", "SD", "OAK", "STL"]

    data = abbr[~abbr["team_abbr"].isin(teams_to_remove)]

    return data["team_abbr"].tolist()
