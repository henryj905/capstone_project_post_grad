import Gathers
import MainFile
import pandas as pd


stats_using_averages = ["completion_percentage", "passer_rating", "efficiency", "yards_per_carry",
                        "yards_per_reception", "yards_per_sack"]
bad_stats = ["interceptions", "fumbles", "sacks", "sack_yards", "sack_fumbles", "yards_per_sack"]


myteamstats = []
opponentstats = []

previous_week_cache = {}


def gather_previous_weeks(team, year, week, stat, use_previous_season=True):
    team = team.upper()
    stat = stat.upper()
    cache_key = (team, year, week, stat)

    if week > 1 and cache_key in previous_week_cache:
        return previous_week_cache[cache_key]

    weekly_funcs = {
        "PASSING": Gathers.passing_gather,
        "RUSHING": Gathers.rushing_gather,
        "RECEIVING": Gathers.receiving_gather,
        "SACKS": Gathers.sacks_gather,
        "SPECIAL": Gathers.special_gather
    }

    season_funcs = {
        "PASSING": Gathers.passing_gather_season,
        "RUSHING": Gathers.rushing_gather_season,
        "RECEIVING": Gathers.receiving_gather_season,
        "SACKS": Gathers.sacks_gather_season,
        "SPECIAL": Gathers.special_gather_season
    }

    if stat not in weekly_funcs:
        return "INVALID STAT CALL"

    if week == 1:
        if use_previous_season:
            result = season_funcs[stat](team, year-1) or {}
        else:
            result = {}
        return [result]

    prev_weeks = gather_previous_weeks(team, year, week - 1, stat, use_previous_season=False)
    result = list(prev_weeks)

    opponent = MainFile.return_opponent(year, team, week - 1)
    if opponent != "BYE":
        last_week = weekly_funcs[stat](team, year, week - 1) or {}
        result.append(last_week)

    previous_week_cache[cache_key] = result
    return result


def combine(stats_list):
    flattened = []
    for week in stats_list:
        if isinstance(week, list):
            flattened.extend([x for x in week if x is not None])
        elif week is not None:
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
        combined[col] = round(df[col].mean(), 2)

    return combined


def torfstatcompare(teamstats, opponent_stats, stat):
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
        return teamstats.get("special_teams_tds", 0) > opponent_stats.get("special_teams_tds", 0)


def compare_weeks(team_stats, opponent_stats):
    team_score = 0
    opponent_score = 0
    for key in team_stats:
        add = torfstatcompare(team_stats, opponent_stats, key)
        if key in bad_stats:
            if key == "interceptions":
                if add == False:
                    team_score += 4
                else:
                    opponent_score += 4
            if key == "fumbles":
                if add == False:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "sacks":
                if add == False:
                    team_score += 4
                else:
                    opponent_score += 4
            if key == "yards_per_sack":
                if add == False:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "sack_fumbles":
                if add == False:
                    team_score += 2
                else:
                    opponent_score += 2
            if key == "sack_yards":
                if add == False:
                    team_score += 2
                else:
                    opponent_score += 2
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
                    team_score += 4
                else:
                    opponent_score += 4
            if key == "passing_tds":
                if add == True:
                    team_score += 3
                else:
                    opponent_score += 3
            if key == "completion_percentage":
                if add == True:
                    team_score += 4
                else:
                    opponent_score += 4
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
                    team_score += 3
                else:
                    opponent_score += 3
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
                    team_score += 3
                else:
                    opponent_score += 3
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
    else:
        return "TIE"
