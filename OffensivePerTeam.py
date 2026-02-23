import playerStatsSeasonal
import pandas as pd

def team_passing_season(team, year):
    team = team.upper()

    pd.set_option('display.max_columns', None)
    data = playerStatsSeasonal.passing_stats_season(year)
    data = data.rename(columns={"recent_team": "team"})
    team_stats = data[data["team"] == team]
    team_stats = data.groupby("team", as_index=False).agg({
        "passing_yards": "sum",
        "completions": "sum",
        "attempts": "sum",
        "passing_tds": "sum",
        "interceptions": "sum",
        "passer_rating": "mean"
    })
    team_stats["passer_rating"] = team_stats["passer_rating"].round(2)
    return team_stats


def team_rushing_season(team, year):
    team = team.upper()

    pd.set_option('display.max_columns', None)
    data = playerStatsSeasonal.rushing_stats_season(year)
    team_stats = data.groupby("recent_team", as_index=False).agg({
        "carries": "sum",
        "rushing_yards": "sum",
        "YPC": "mean",
        "rushing_tds": "sum",
        "rushing_fumbles": "sum",
        "rushing_fumbles_lost": "sum",
        "efficiency": "mean"
    })
    team_stats = team_stats.rename(columns={"recent_team": "team_abbr"})
    team_stats = team_stats[team_stats["team"] == team]
    team_stats["YPC"] = team_stats["YPC"].round(2)
    team_stats["efficiency"] = team_stats["efficiency"].round(2)
    return team_stats

def team_receiving_season(team, year):
    team = team.upper()

    pd.set_option('display.max_columns', None)
    data = playerStatsSeasonal.receiving_stats_season(year)
    team_stats = data.groupby("recent_team", as_index=False).agg({
        "receptions": "sum",
        "targets": "sum",
        "receiving_yards": "sum",
        "receiving_yards_after_catch": "sum",
        "receiving_tds": "sum",
        "avg_completion_pct": "mean",
        "avg_yards_per_rec": "mean",
        "avg_separation": "mean"
    })
    team_stats = team_stats.rename(columns={"recent_team": "team_abbr"})
    team_stats = team_stats[team_stats["team"] == team]
    team_stats["avg_completion_pct"] = team_stats["avg_completion_pct"].round(2)
    team_stats["avg_yards_per_rec"] = team_stats["avg_yards_per_rec"].round(2)
    team_stats["avg_separation"] = team_stats["avg_separation"].round(2)
    return team_stats

def team_sacks_season(team, year):
    team = team.upper()
    pd.set_option('display.max_columns', None)
    data = playerStatsSeasonal.sacks_by_qb_season(year)
    team_stats = data.groupby("recent_team", as_index=False).agg({
        "sacks": "sum",
        "sack_yards": "sum",
        "sack_fumbles": "sum",
        "sack_fumbles_lost": "sum"
    })
    team_stats = team_stats.rename(columns={"recent_team": "team_abbr"})
    team_stats = team_stats[team_stats["team"] == team]
    team_stats["fumble_lost_ratio"] = (team_stats["sack_fumbles_lost"]/team_stats["sack_fumbles"]).round(2)


    return team_stats

print(team_passing_season('was', 2024))