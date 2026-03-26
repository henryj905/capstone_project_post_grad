import nfl_data_py as nfl
import pandas as pd


weekly_cache = {}
ngs_cache = {}

def get_weekly_data(year):
    if year not in weekly_cache:
        weekly_cache[year] = nfl.import_weekly_data([year])
    return weekly_cache[year]

def get_ngs_data(stat_type, year):
    key = (stat_type, year)
    if key not in ngs_cache:
        ngs_cache[key] = nfl.import_ngs_data(stat_type, [year])
    return ngs_cache[key]


def passing_weekly(year, week, name):
    weekly = get_weekly_data(year)
    weekly = weekly[["week", "player_id", "player_name", "recent_team", "position", "completions", "attempts", "passing_yards",
                     "passing_tds", "interceptions"]]
    efficiency = nfl.import_ngs_data("passing", [year])
    efficiency = efficiency[["player_gsis_id", "completion_percentage", "passer_rating", "week"]]
    efficiency = efficiency.rename(columns={"player_gsis_id": "player_id"})
    efficiency = efficiency.drop_duplicates()
    weekly = weekly.merge(
        efficiency,
        on=["player_id", "week"],
        how="left"
    )

    weekly = weekly[weekly["attempts"] > 0]
    weekly = weekly[weekly["week"] == week]
    weekly = weekly[weekly["player_name"]==name]
    return weekly.sort_values(["recent_team", "position"])


def rushing_weekly(year, week, name):
    weekly = get_weekly_data(year)
    weekly = weekly[["week", "player_id", "player_name", "recent_team", "position", 'carries', 'rushing_yards', 'rushing_tds', 'rushing_fumbles']]
    efficiency = nfl.import_ngs_data("rushing", [year])
    efficiency = efficiency[["player_gsis_id", "efficiency", "week"]]
    efficiency = efficiency.rename(columns={"player_gsis_id": "player_id"})
    efficiency = efficiency.drop_duplicates()
    weekly = weekly.merge(
        efficiency,
        on=["player_id", "week"],
        how="left"
    )

    weekly = weekly[weekly["carries"] > 0]
    weekly = weekly[weekly["week"] == week]
    weekly = weekly[weekly["player_name"]==name]


    return weekly.sort_values(["recent_team", "position", "player_name"])


def receiving_weekly(year, week, name):
    weekly = get_weekly_data(year)
    weekly = weekly[
        ["week", "player_id", "player_name", "recent_team", "position", 'targets', 'receptions', 'receiving_yards',
         'receiving_tds']]

    weekly = weekly[weekly["targets"] > 0]
    weekly = weekly[weekly["week"] == week]
    weekly = weekly[weekly["player_name"]==name]


    return weekly.sort_values(["recent_team", "position", "player_name"])

def sacks_qb_weekly(year, week, name):
    sacks = get_weekly_data(year)
    sacks = sacks[["week", "player_id", "player_name", "recent_team", "position", "sacks", "sack_yards", "sack_fumbles"]]

    sacks = sacks[sacks["sacks"] > 0]
    sacks = sacks[sacks["week"] == week]
    sacks = sacks[sacks["player_name"]==name]

    return sacks.sort_values(["recent_team", "position", "player_name"])


def special_tds_weekly(year, week, name):
    special = get_weekly_data(year)
    special = special[["week", "player_id", "player_name", "recent_team", "special_teams_tds"]]

    special = special[special["special_teams_tds"] > 0]
    special = special[special["week"] == week]
    special = special[special["player_name"]==name]

    return special.sort_values(["recent_team", "player_name"])
