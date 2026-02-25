import OffensivePerTeam
import OffensiveTeamWeekly
import MainFile


def week_opponent(year, team, week):
    schedule = MainFile.team_schedule(year, team)

    schedule = schedule[schedule["week"] == week]

    if schedule["home_team"].values[0] == team.upper():
        opponent = schedule["away_team"].values[0]
    else:
        opponent = schedule["home_team"].values[0]

    return opponent


def passing_compare(team1, team2, team1stats, team2stats):
    results = {}

    for col in team1stats.select_dtypes(include="number").columns:

        team1passing = team1stats[col].iloc[0]
        team2passing = team2stats[col].iloc[0]

        if col == "interceptions":
            print(team1, team1passing, team2, team2passing)
            if team1passing > team2passing:
                winner = team2
            elif team1passing < team2passing:
                winner = team1
            else:
                winner = "TIE"

        else:
            if team1passing > team2passing:
                winner = team1
            elif team1passing < team2passing:
                winner = team2
            else:
                winner = "TIE"

        results[col] = winner
    return results


def rushing_compare(team1, team2, team1stats, team2stats):
    results = {}

    for col in team1stats.select_dtypes(include="number").columns:

        team1rushing = team1stats[col].iloc[0]
        team2rushing = team2stats[col].iloc[0]

        if col == "rushing_fumbles":
            if team1rushing > team2rushing:
                winner = team2
            elif team1rushing < team2rushing:
                winner = team1
            else:
                winner = "TIE"

        else:
            if team1rushing > team2rushing:
                winner = team1
            elif team1rushing < team2rushing:
                winner = team2
            else:
                winner = "TIE"

        results[col] = winner
    return results


def receiving_compare(team1, team2, team1stats, team2stats):
    results = {}

    for col in team1stats.select_dtypes(include="number").columns:
        team1receiving = team1stats[col].iloc[0]
        team2receiving = team2stats[col].iloc[0]

        if team1receiving > team2receiving:
            winner = team1
        elif team1receiving < team2receiving:
            winner = team2
        else:
            winner = "TIE"

        results[col] = winner

    return results

def sacks_compare(team1, team2, team1stats, team2stats):
    results = {}

    for col in team1stats.select_dtypes(include="number").columns:

        team1sacks = team1stats[col].iloc[0]
        team2sacks = team2stats[col].iloc[0]

        if team1sacks > team2sacks:
            winner = team2
        elif team1sacks < team2sacks:
            winner = team1
        else:
            winner = "TIE"

        results[col] = winner
    return results

def special_compare(team1, team2, team1stats, team2stats):
    results = {}

    if team1stats.empty and team2stats.empty:
        return {"special_teams_tds": "TIE"}

    if team1stats.empty:
        return {"special_teams_tds": team2}

    if team2stats.empty:
        return {"special_teams_tds": team1}

    for col in team1stats.select_dtypes(include="number").columns:

        team1special = team1stats[col].iloc[0]
        team2special = team2stats[col].iloc[0]

        if team1special > team2special:
            winner = team1
        elif team1special < team2special:
            winner = team2
        else:
            winner = "TIE"

        results[col] = winner
    return results
def compare_year(team1, team2, year, week, stat):
    stat = stat.upper()
    team1 = team1.upper()
    team2 = team2.upper()

    if week < 2:
        stat_functions = {
            "PASSING": OffensivePerTeam.team_passing_season,
            "RUSHING": OffensivePerTeam.team_rushing_season,
            "RECEIVING": OffensivePerTeam.team_receiving_season,
            "SACKS": OffensivePerTeam.team_sacks_season,
            "SPECIAL": OffensivePerTeam.team_special_tds_season
        }
        func = stat_functions.get(stat)
        team1Stats = func(team1, year)
        team2Stats = func(team2, year)

    else:
        team1Stats = OffensiveTeamWeekly.team_weekly_stats(team1, year, week, stat)
        team2Stats = OffensiveTeamWeekly.team_weekly_stats(team2, year, week, stat)

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
    stat = 'special'
    opponent = week_opponent(year, myteam, week)
    print(compare_year(myteam, opponent, year, week, stat))
