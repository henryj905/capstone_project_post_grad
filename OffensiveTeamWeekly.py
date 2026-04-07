import playerWeeklyStats
import pandas as pd


def team_weekly_stats(team, year, week, stat):
    team = team.upper()
    stat = stat.upper()

    data_sets = {
        "PASSING": playerWeeklyStats.passing_weekly,
        'RUSHING': playerWeeklyStats.rushing_weekly,
        'RECEIVING': playerWeeklyStats.receiving_weekly,
        'SACKS': playerWeeklyStats.sacks_qb_weekly,
        'SPECIAL': playerWeeklyStats.special_tds_weekly
    }
    data = []
    while week != 0:
        func = data_sets.get(stat)
        function = func(year, week, team)

        function = function.drop(columns=["player_id", "player_name"])

        function = function.groupby("recent_team", as_index=False).sum(numeric_only=True)
        data.append(function)
        week -= 1

    function = pd.concat(data, ignore_index=True)
    my_dict = {}
    if stat == "PASSING":
        my_dict = {
            "passing_yards": "sum",
            "completions": "sum",
            "attempts": "sum",
            "passing_tds": "sum",
            "interceptions": "sum",
            "passer_rating": "mean"  # average passer rating
        }
    elif stat == "RUSHING":
        my_dict = {
            "carries": "sum",
            "rushing_yards": "sum",
            "rushing_tds": "sum",
            "rushing_fumbles": "sum",
            "efficiency": "mean"
        }
    elif stat == "RECEIVING":
        my_dict = {
            "receptions": "sum",
            "targets": "sum",
            "receiving_yards": "sum",
            "receiving_tds": "sum",
        }
    elif stat == "SACKS":
        my_dict = {
            "sacks": "sum",
            "sack_yards": "sum",
            "sack_fumbles": "sum",
        }
    elif stat == "SPECIAL":
        my_dict = {
            "special_teams_tds": "sum"
        }

    function = function.groupby("recent_team", as_index=False).agg(my_dict)
    function = function[function["recent_team"] == team]
    return function
