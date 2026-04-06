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

    bad_stat_points = {
        "interceptions": 4,
        "fumbles": 3,
        "sacks": 4,
        "yards_per_sack": 2,
        "sack_fumbles": 3,
        "sack_yards": 2
    }

    good_stat_points = {
        "completions": 2,
        "attempts": 1,
        "passing_yards": 3,
        "passing_tds": 3,
        "completion_percentage": 4,
        "passer_rating": 3,
        "carries": 1,
        "rushing_yards": 6,
        "rushing_tds": 3,
        "yards_per_carry": 2,
        "efficiency": 3,
        "targets": 1,
        "receiving_yards": 2,
        "receiving_tds": 2,
        "yards_per_reception": 3,
        "special_teams_tds": 2
    }

    for key in team_stats:
        add = torfstatcompare(team_stats, opponent_stats, key)

        if key in bad_stat_points:
            points = bad_stat_points[key]
            if add is False:
                team_score += points
            else:
                opponent_score += points
        elif key in good_stat_points:
            points = good_stat_points[key]
            if add is True:
                team_score += points
            else:
                opponent_score += points

    return team_score, opponent_score


def return_winner(team1, team1score, team2, team2score):
    if team1score > team2score:
        return team1
    elif team2score > team1score:
        return team2
    else:
        return "TIE"

def run(year, week, team):
    stats = ["passing", "rushing", "receiving", "sacks", "special"]
    rows = []

    team1stat = []
    team2stat = []
    if MainFile.return_opponent(year, team, week) == "BYE":
        rows.append({
            "team": team,
            "team_score": None,
            "opponent": None,
            "opponent_score": None,
            "predicted_winner": None
        })
    for stat in stats:
        team1 = gather_previous_weeks(team, year, week, stat)
        team2 = gather_previous_weeks(MainFile.return_opponent(year, team, week), year, week, stat)
        team1 = combine(team1)
        team2 = combine(team2)
        team1stat.append(team1)
        team2stat.append(team2)

    team1score = 0
    team2score = 0
    for t1, t2 in zip(team1stat, team2stat):
        t1score, t2score = compare_weeks(t1, t2)
        team1score += t1score
        team2score += t2score


    team_score = team1score
    opponent = MainFile.return_opponent(year, team, week)
    opponent_score = team2score
    winner = return_winner(team, team_score, opponent, opponent_score)

    rows.append({
        "team": team,
        "team_score": team_score,
        "opponent": opponent,
        "opponent_score": opponent_score,
        "predicted_winner": winner
    })

    df = pd.DataFrame(rows)

    return df
