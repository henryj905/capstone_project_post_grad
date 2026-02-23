import OffensivePerTeam
import OffensiveTeamWeekly
import MainFile


def week_opponent(year, team, week):
    stats = OffensivePerTeam.team_passing_season(year)
    schedule = MainFile.team_schedule(year, team)

    schedule = schedule[schedule["week"] == week]

    if schedule["home_team"].values[0] == team.upper():
        opponent = schedule["away_team"].values[0]
    else:
        opponent = schedule["home_team"].values[0]

    return opponent

def compare_year(team1, team2, year, week, stat):
    stat = stat.upper()
    team1 = team1.upper()
    team2 = team2.upper()
    team1Stats = ""
    team2Stats = ""
    if week < 2:
        stat_functions = {
            "PASSING": OffensivePerTeam.team_passing_season,
            "RUSHING": OffensivePerTeam.team_rushing_season,
            "RECEIVING": OffensivePerTeam.team_receiving_season,
            "SACKS": OffensivePerTeam.team_sacks_season
        }
        func = stat_functions.get(stat)
        team1Stats = func(team1, year)
        team2Stats = func(team2, year)

    else:
        team1Stats = OffensiveTeamWeekly.team_weekly_stats(team1, year, week, stat)
        team2Stats = OffensiveTeamWeekly.team_weekly_stats(team2, year, week, stat)

    team1passing = team1Stats["passing_yards"].iloc[0]
    team2passing = team2Stats["passing_yards"].iloc[0]

    if team1passing > team2passing:
        passing_compare = team1
    else:
        passing_compare = team2

    return passing_compare

def points_for_passing(year, team, week):
    opponent = week_opponent(year, team, week)

    return None


if __name__ == "__main__":
#    print(week_opponent(2019, 'bal', 13))
    print(compare_year('was', 'bal', 2024, 1, 'passing'))