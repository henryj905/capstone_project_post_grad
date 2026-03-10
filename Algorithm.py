import playerWeeklyStats
import MainFile
import InLists
import pandas as pd


stats_using_averages = ["completion_percentage", "passer_rating", "efficiency", "yards_per_carry", "yards_per_reception", "yards_per_sack"]
bad_stats = ["interceptions", "rushing_fumbles", "sack_fumbles", "yards_per_sack"]
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

    passer_rating = team_df["passer_rating"].mean().round(2)

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
    mean_efficiency = team_df["efficiency"].mean().round(2)

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
            "special_teams_tds":0
        })

    else:
        team_df = pd.concat(dfs, ignore_index=True)
        total_tds = team_df["special_teams_tds"].sum()

        team_stats.append({
            "special_tams_tds": total_tds
        })
    return team_stats

myteamstats = []
opponentstats = []
def gather_previous_weeks(team, year, week, stat):
    team = team.upper()
    stat = stat.upper()
    opponent = MainFile.return_opponent(year, team, week)

    stat_functions = {
        "PASSING": passing_gather,
        "RUSHING": rushing_gather,
        "RECEIVING": receiving_gather,
        "SACKS": sacks_gather,
        "SPECIAL": special_gather
    }
    if stat not in stat_functions:
        return "INVALID STAT CALL"

    func = stat_functions.get(stat)
    if week == 1:
        return [], []

    team_prev, opp_prev = gather_previous_weeks(team, year, week - 1, stat)
    team_last_week = func(team, year, week - 1)
    opp_last_week = func(opponent, year, week - 1)
    team_prev.append(team_last_week)
    opp_prev.append(opp_last_week)

    return team_prev, opp_prev


def combine_weeks(stats_list):
    flattened = []
    for week in stats_list:
        if isinstance(week, list):
            flattened.extend(week)
        else:
            flattened.append(week)

    if not flattened:
        return {}

    df = pd.DataFrame(flattened)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    sum_cols = [c for c in numeric_cols if c not in stats_using_averages]
    avg_cols = [c for c in numeric_cols if c in stats_using_averages]
    combined = {}

    for col in sum_cols:
        combined[col] = df[col].sum()
    for col in avg_cols:
        combined[col] = df[col].mean().round(2)

    return combined


def compare_weeks(team_stats, opponent_stats):
    team_score = 0
    opponent_score = 0

    for key in team_stats:
        if key not in opponent_stats:
            continue
    # may hard code here to have different values assigned to different stats
    # for example 3 points for passing yards but 1 for completions
        if key in bad_stats:
            print(key)
            if team_stats[key] < opponent_stats[key]:
                team_score += 1
            elif team_stats[key] > opponent_stats[key]:
                opponent_score += 1
        else:
            print(key)
            if team_stats[key] > opponent_stats[key]:
                team_score += 1
            elif team_stats[key] < opponent_stats[key]:
                opponent_score += 1

    return team_score, opponent_score

if __name__ == "__main__":
    year = 2024
    week = 3
    myteam = "was"
    stats = ["passing", "rushing", "receiving", "sacks", "special"]

    team1stat = []
    team2stat = []
    for stat in stats:
        team1, team2 = gather_previous_weeks(myteam, year, week, stat)
        team1 = combine_weeks(team1)
        team2 = combine_weeks(team2)
        team1stat.append(team1)
        team2stat.append(team2)

    team1score = 0
    team2score = 0
    for t1, t2 in zip(team1stat, team2stat):
        t1score, t2score = compare_weeks(t1, t2)
        team1score += t1score
        team2score += t2score
    print(team1score, team2score)