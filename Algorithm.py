import playerWeeklyStats
import playerStatsSeasonal
import MainFile
import InLists
import pandas as pd

def week_opponent(year, team, week):
    schedule = MainFile.team_schedule(year, team)

    schedule = schedule[schedule["week"] == week]

    if schedule["home_team"].values[0] == team.upper():
        opponent = schedule["away_team"].values[0]
    else:
        opponent = schedule["home_team"].values[0]

    return opponent


def passing_compare(team1, team2, year, week):
    team1 = team1.upper()
    team2 = team2.upper()

    teams = [team1, team2]
    team_stats = []
    for team in teams:
        dfs = []

        for _, row in InLists.player_in_passing(year, week, team).iterrows():
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


def rushing_compare(team1, team2, year, week):
    team1 = team1.upper()
    team2 = team2.upper()

    teams = [team1, team2]
    team_stats = []
    for team in teams:
        dfs = []

        for _, row in InLists.player_in_rushing(year, week, team).iterrows():
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


def receiving_compare(team1, team2, year, week):
    team1 = team1.upper()
    team2 = team2.upper()

    teams = [team1, team2]
    team_stats = []
    for team in teams:
        dfs = []

        for _, row in InLists.player_in_receiving(year, week, team).iterrows():
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


def sacks_compare(team1, team2, year, week):
    team1 = team1.upper()
    team2 = team2.upper()

    teams = [team1, team2]
    team_stats = []
    for team in teams:
        dfs = []

        for _, row in InLists.player_in_sacks(year, week, team).iterrows():
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
            print(list(team_df.columns))
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


def special_compare(team1, team2, year, week):
    team1 = team1.upper()
    team2 = team2.upper()

    teams = [team1, team2]
    team_stats = []
    for team in teams:
        dfs = []

        for _, row in InLists.player_in_special(year, week, team).iterrows():
            df = playerWeeklyStats.special_tds_weekly(year, week, row["player_name"])
            if not df.empty:
                dfs.append(df)

        if not dfs:
            team_stats.append({
                "special_teams_tds":0
            })

        else:
            team_df = pd.concat(dfs, ignore_index=True)
            print(list(team_df.columns))
            total_tds = team_df["special_teams_tds"].sum()

            team_stats.append({
                "special_tams_tds": total_tds
            })
    return team_stats


def compare_year(team1, team2, year, week, stat):
    stat = stat.upper()
    team1 = team1.upper()
    team2 = team2.upper()
    if week < 2:
        stat_functions = {
            "PASSING": playerWeeklyStats.passing_weekly,
            "RUSHING": playerWeeklyStats.rushing_weekly,
            "RECEIVING": playerWeeklyStats.receiving_weekly,
            "SACKS": playerWeeklyStats.sacks_qb_weekly,
            "SPECIAL": playerWeeklyStats.special_tds_weekly
        }
        func = stat_functions.get(stat)
        team1Stats = func(year, week, team1)
        team2Stats = func(year, week, team2)

    else:
        stat_functions = {
            "PASSING": playerStatsSeasonal.passing_stats_season,
            "RUSHING": playerStatsSeasonal.rushing_stats_season,
            "RECEIVING": playerStatsSeasonal.receiving_stats_season,
            "SACKS": playerStatsSeasonal.sacks_by_qb_season,
            "SPECIAL": playerStatsSeasonal.special_teams_tds_season
        }
        func = stat_functions.get(stat)
        team1Stats = func(team1, year)
        team2Stats = func(team2, year)
    return_options = {
        "PASSING": passing_compare,
        "RUSHING": rushing_compare,
        "RECEIVING": receiving_compare,
        "SACKS": sacks_compare,
        "SPECIAL": special_compare
    }
    func = return_options.get(stat)
    return func(team1, team2, team1Stats, team2Stats)


if __name__ == "__main__":
    year = 2024
    week = 2
    myteam = 'was'
    stat = 'passing'
    opponent = week_opponent(year, myteam, week)
    result = compare_year(myteam, opponent, year, week, stat)

    print(myteam, opponent, result)