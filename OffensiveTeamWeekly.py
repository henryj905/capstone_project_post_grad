import OffensiveStatsWeekly
import pandas as pd
import MainFile

def team_weekly_stats(team, year, week, stat):
    team = team.upper()
    stat = stat.upper()

    data_sets = {
        "PASSING": OffensiveStatsWeekly.passing_weekly,
        'RUSHING': OffensiveStatsWeekly.rushing_weekly,
        'RECEIVING': OffensiveStatsWeekly.receiving_weekly,
        'SACKS': OffensiveStatsWeekly.sacks_qb_weekly
    }
    data = []
    while week!=0:
        func = data_sets.get(stat)
        function = func(year, week)

        function = function.drop(columns=["player_id", "player_name"])

        function = function.groupby("recent_team", as_index=False).sum(numeric_only=True)
        data.append(function)
        week -= 1

    function = pd.concat(data, ignore_index=True)
    dict = {}
    if stat == "PASSING":
        dict = {
            "passing_yards": "sum",
            "completions": "sum",
            "attempts": "sum",
            "passing_tds": "sum",
            "interceptions": "sum",
            "passer_rating": "mean"  # average passer rating
        }
    elif stat == "RUSHING":
        dict = {
            "carries": "sum",
            "rushing_yards": "sum",
            "rushing_tds": "sum",
            "rushing_fumbles": "sum",
            "efficiency": "mean"
        }
    elif stat == "RECEIVING":
        dict = {
            "receptions": "sum",
            "targets": "sum",
            "receiving_yards": "sum",
            "receiving_tds": "sum",
        }
    elif stat == "SACKS":
        dict = {
            "sacks": "sum",
            "sack_yards": "sum",
            "sack_fumbles": "sum",
        }

    function = function.groupby("recent_team", as_index=False).agg(dict)
    function = function[function["recent_team"] == team]
    return function