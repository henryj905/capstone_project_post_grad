import pandas as pd
import InLists
import playerWeeklyStats
import playerStatsSeasonal


def passing_gather(team1, year, week):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_passing(year, week, team1).iterrows():
        df = playerWeeklyStats.passing_weekly(year, week, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return None

    team_df = pd.concat(dfs, ignore_index=True)

    total_completions = team_df["completions"].sum()
    total_attempts = team_df["attempts"].sum()
    total_yards = team_df["passing_yards"].sum()
    total_tds = team_df["passing_tds"].sum()
    total_ints = team_df["interceptions"].sum()

    completion_pct = (
        total_completions / total_attempts
        if total_attempts > 0 else 0
     ).round(2)

    passer_rating = round(team_df["passer_rating"].mean(), 2)

    team_stats.append({
        "completions": total_completions,
        "attempts": total_attempts,
        "passing_yards": total_yards,
        "passing_tds": total_tds,
        "interceptions": total_ints,
        "completion_percentage": completion_pct,
        "passer_rating": passer_rating
    })
    return team_stats


def rushing_gather(team1, year, week):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_rushing(year, week, team1).iterrows():
        df = playerWeeklyStats.rushing_weekly(year, week, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return None

    team_df = pd.concat(dfs, ignore_index=True)
    total_carries = team_df["carries"].sum()
    total_yards = team_df["rushing_yards"].sum()
    total_tds = team_df["rushing_tds"].sum()
    total_fumbles = team_df["rushing_fumbles"].sum()
    mean_efficiency = round(team_df["efficiency"].mean(), 2)

    ypc = (
        total_yards / total_carries
    ).round(2)

    team_stats.append({
        "carries": total_carries,
        "rushing_yards": total_yards,
        "rushing_tds": total_tds,
        "fumbles": total_fumbles,
        "yards_per_carry": ypc,
        "efficiency": mean_efficiency
    })
    return team_stats


def receiving_gather(team1, year, week):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_receiving(year, week, team1).iterrows():
        df = playerWeeklyStats.receiving_weekly(year, week, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return None

    team_df = pd.concat(dfs, ignore_index=True)
    total_targets = team_df["targets"].sum()
    total_receptions = team_df["receptions"].sum()
    total_yards = team_df["receiving_yards"].sum()
    total_tds = team_df["receiving_tds"].sum()

    ypr = (
        total_yards / total_receptions
    ).round(2)

    team_stats.append({
        "targets": total_targets,
        "receiving_yards": total_yards,
        "receiving_tds": total_tds,
        "yards_per_reception": ypr
    })
    return team_stats


def sacks_gather(team1, year, week):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_sacks(year, week, team1).iterrows():
        df = playerWeeklyStats.sacks_qb_weekly(year, week, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        team_stats.append({
            "sacks": 0,
            "sack_yards": 0,
            "sack_fumbles": 0,
            "yards_per_sack": 0
        })

    else:
        team_df = pd.concat(dfs, ignore_index=True)
        total_sacks = team_df["sacks"].sum()
        total_sack_yards = team_df["sack_yards"].sum()
        total_fumbles = team_df["sack_fumbles"].sum()

        yps = (
            total_sack_yards / total_sacks
        ).round(2)

        team_stats.append({
            "sacks": total_sacks,
            "sack_yards": total_sack_yards,
            "sack_fumbles": total_fumbles,
            "yards_per_sack": yps
        })
    return team_stats


def special_gather(team1, year, week):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_special(year, week, team1).iterrows():
        df = playerWeeklyStats.special_tds_weekly(year, week, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        team_stats.append({
            "special_teams_tds": 0
        })

    else:
        team_df = pd.concat(dfs, ignore_index=True)
        total_tds = team_df["special_teams_tds"].sum()

        team_stats.append({
            "special_tams_tds": total_tds
        })
    return team_stats


def passing_gather_season(team1, year):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_passing_season(year - 1, team1).iterrows():
        df = playerStatsSeasonal.passing_stats_season(year -1, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return None

    team_df = pd.concat(dfs, ignore_index=True)

    total_completions = team_df["completions"].sum()
    total_attempts = team_df["attempts"].sum()
    total_yards = team_df["passing_yards"].sum()
    total_tds = team_df["passing_tds"].sum()
    total_ints = team_df["interceptions"].sum()

    completion_pct = (
        total_completions / total_attempts
        if total_attempts > 0 else 0
     ).round(2)

    passer_rating = round(team_df["passer_rating"].mean(), 2)

    team_stats.append({
        "completions": total_completions,
        "attempts": total_attempts,
        "passing_yards": total_yards,
        "passing_tds": total_tds,
        "interceptions": total_ints,
        "completion_percentage": completion_pct,
        "passer_rating": passer_rating
    })
    return team_stats


def rushing_gather_season(team1, year):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_rushing_season(year-1, team1).iterrows():
        df = playerStatsSeasonal.rushing_stats_season(year-1, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return None

    team_df = pd.concat(dfs, ignore_index=True)
    total_carries = team_df["carries"].sum()
    total_yards = team_df["rushing_yards"].sum()
    total_tds = team_df["rushing_tds"].sum()
    total_fumbles = team_df["rushing_fumbles"].sum()
    mean_efficiency = round(team_df["efficiency"].mean(), 2)

    ypc = (
        total_yards / total_carries
    ).round(2)

    team_stats.append({
        "carries": total_carries,
        "rushing_yards": total_yards,
        "rushing_tds": total_tds,
        "fumbles": total_fumbles,
        "yards_per_carry": ypc,
        "efficiency": mean_efficiency
    })
    return team_stats


def receiving_gather_season(team1, year):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_receiving_season(year - 1, team1).iterrows():
        df = playerStatsSeasonal.receiving_stats_season(year - 1, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return None

    team_df = pd.concat(dfs, ignore_index=True)
    total_targets = team_df["targets"].sum()
    total_receptions = team_df["receptions"].sum()
    total_yards = team_df["receiving_yards"].sum()
    total_tds = team_df["receiving_tds"].sum()

    ypr = (
        total_yards / total_receptions
    ).round(2)

    team_stats.append({
        "targets": total_targets,
        "receiving_yards": total_yards,
        "receiving_tds": total_tds,
        "yards_per_reception": ypr
    })
    return team_stats


def sacks_gather_season(team1, year):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_sacks_season(year - 1, team1).iterrows():
        df = playerStatsSeasonal.sacks_by_qb_season(year - 1, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        team_stats.append({
            "sacks": 0,
            "sack_yards": 0,
            "sack_fumbles": 0,
            "yards_per_sack": 0
        })

    else:
        team_df = pd.concat(dfs, ignore_index=True)
        total_sacks = team_df["sacks"].sum()
        total_sack_yards = team_df["sack_yards"].sum()
        total_fumbles = team_df["sack_fumbles"].sum()

        yps = (
            total_sack_yards / total_sacks
        ).round(2)

        team_stats.append({
            "sacks": total_sacks,
            "sack_yards": total_sack_yards,
            "sack_fumbles": total_fumbles,
            "yards_per_sack": yps
        })
    return team_stats


def special_gather_season(team1, year):
    team1 = team1.upper()

    team_stats = []
    dfs = []

    for _, row in InLists.player_in_special_season(year - 1, team1).iterrows():
        df = playerStatsSeasonal.special_teams_tds_season(year - 1, row["player_name"])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        team_stats.append({
            "special_teams_tds": 0
        })

    else:
        team_df = pd.concat(dfs, ignore_index=True)
        total_tds = team_df["special_teams_tds"].sum()

        team_stats.append({
            "special_tams_tds": total_tds
        })
    return team_stats
