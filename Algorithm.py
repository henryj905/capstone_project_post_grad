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
    if week < 2:
        stat_functions = {
            "PASSING": OffensivePerTeam.team_passing_season,
            "RUSHING": OffensivePerTeam.team_rushing_season,
            "RECEIVING": OffensivePerTeam.team_receiving_season,
            "SACKS": OffensivePerTeam.team_sacks_season
        }
    else:
        stat_functions = {
            "PASSING": OffensiveTeamWeekly.team_weekly_stats,
            "RUSHING": OffensiveTeamWeekly.team_weekly_stats,
            "RECEIVING": OffensiveTeamWeekly.team_weekly_stats,
            "SACKS": OffensiveTeamWeekly.team_weekly_stats
        }

    return None

def points_for_passing(year, team, week):
    opponent = week_opponent(year, team, week)

    return None


if __name__ == "__main__":
#    print(week_opponent(2019, 'bal', 13))
    print(compare_year('was', 'bal', 2024, 1, 'passing'))