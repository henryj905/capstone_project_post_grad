import playerWeeklyStats
import MainFile
import InLists
import pandas as pd


stats_using_averages = ["completion_percentage", "passer_rating", "efficiency", "yards_per_carry", "yards_per_reception", "yards_per_sack"]
bad_stats = ["interceptions", "fumbles", "sacks", "sack_yards", "sack_fumbles", "yards_per_sack"]
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


def TorFStatCompare(teamstats, opponent_stats, stat):
    if stat == "completions":
        return teamstats["completions"] > opponent_stats["completions"]
    if stat == "attempts":
        return teamstats["attempts"] > opponent_stats["attempts"]
    if stat == "passing_yards":
        return teamstats["passing_yards"] > opponent_stats["passing_yards"]
    if stat == "passing_tds":
        return teamstats["passing_tds"] > opponent_stats["passing_tds"]
    if stat == "interceptions":
        return teamstats["interceptions"] > opponent_stats["interceptions"]
    if stat == "completion_percentage":
        return teamstats["completion_percentage"] > opponent_stats["completion_percentage"]
    if stat == "passer_rating":
        return teamstats["passer_rating"] > opponent_stats["passer_rating"]
    if stat == "carries":
        return teamstats["carries"] > opponent_stats["carries"]
    if stat == "rushing_yards":
        return teamstats["rushing_yards"] > opponent_stats["rushing_yards"]
    if stat == "rushing_tds":
        return teamstats["rushing_tds"] > opponent_stats["rushing_tds"]
    if stat == "fumbles":
        return teamstats["fumbles"] > opponent_stats["fumbles"]
    if stat == "yards_per_carry":
        return teamstats["yards_per_carry"] > opponent_stats["yards_per_carry"]
    if stat == "efficiency":
        return teamstats["efficiency"] > opponent_stats["efficiency"]
    if stat == "targets":
        return teamstats["targets"] > opponent_stats["targets"]
    if stat == "receiving_yards":
        return teamstats["receiving_yards"] > opponent_stats["receiving_yards"]
    if stat == "receiving_tds":
        return teamstats["receiving_tds"] > opponent_stats["receiving_tds"]
    if stat == "yards_per_reception":
        return teamstats["yards_per_reception"] > opponent_stats["yards_per_reception"]
    if stat == "sacks":
        return teamstats["sacks"] > opponent_stats["sacks"]
    if stat == "sack_yards":
        return teamstats["sack_yards"] > opponent_stats["sack_yards"]
    if stat == "sack_fumbles":
        return teamstats["sack_fumbles"] > opponent_stats["sack_fumbles"]
    if stat == "yards_per_sack":
        return teamstats["yards_per_sack"] > opponent_stats["yards_per_sack"]
    if stat == "special_teams_tds":
        return teamstats["special_teams_tds"] > opponent_stats["special_teams_tds"]


def compare_weeks(team_stats, opponent_stats):
    team_score = 0
    opponent_score = 0
    for key in team_stats:
        add = TorFStatCompare(team_stats, opponent_stats, key)
        if key in bad_stats:
            if key == "interceptions":
                if add == False:
                    team_score += 3
                else: opponent_score += 3
            if key == "fumbles":
                if add == False:
                    team_score += 1
                else: opponent_score += 1
            if key == "sacks":
                if add == False:
                    team_score += 4
                else: opponent_score += 4
            if key == "yards_per_sack":
                if add == False:
                    team_score += 2
                else: opponent_score += 2
            if key == "sack_fumbles":
                if add == False:
                    team_score += 1
                else: opponent_score += 1
            if key == "sack_yards":
                if add ==False:
                    team_score += 2
                else: opponent_score += 2
        else:
            if key == "completions":
                if add == True:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "attempts":
                if add == True:
                    team_score += 1
                else:
                    opponent_score += 1
            if key == "passing_yards":
                if add == True:
                    team_score += 5
                else:
                    opponent_score += 5
            if key == "passing_tds":
                if add == True:
                    team_score += 3
                else:
                    opponent_score += 3
            if key == "completion_percentage":
                if add == True:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "passer_rating":
                if add == True:
                    team_score += 3
                else:
                    opponent_score += 3
            if key == "carries":
                if add == True:
                    team_score += 1
                else:
                    opponent_score += 1
            if key == "rushing_yards":
                if add == True:
                    team_score += 4
                else:
                    opponent_score += 4
            if key == "rushing_tds":
                if add == True:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "yards_per_carry":
                if add == True:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "efficiency":
                if add == True:
                    team_score += 1
                else:
                    opponent_score += 1
            if key == "targets":
                if add == True:
                    team_score += 1
                else:
                    opponent_score += 1
            if key == "receiving_yards":
                if add == True:
                    team_score += 3
                else:
                    opponent_score += 3
            if key == "receiving_tds":
                if add == True:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "yards_per_reception":
                if add == True:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "special_teams_tds":
                if add == True:
                    team_score += 1
                else:
                    opponent_score += 1
    return team_score, opponent_score


def return_winner(team1, team1score, team2, team2score):
    if team1score > team2score:
        return team1
    elif team2score > team1score:
        return team2
    else: return "TIE"


if __name__ == "__main__":
    year = 2024
    week = 6
    myteam = "was".upper()
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

    print(myteam, team1score)
    print(MainFile.return_opponent(year, myteam, week), team2score)
    print("Predicted winner: ", return_winner(myteam, team1score, MainFile.return_opponent(year, myteam, week), team2score))
