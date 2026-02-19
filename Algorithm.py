import OffensivePerTeam
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
    if week < 3:
        stats = OffensivePerTeam.team_passing_season(year-1)
    else:


    if stat not in stats.columns:
        return f"input not valid, select input from: {list(stats.columns)}"

    team1value = stats.loc[stats["recent_team"].str.upper() == team1.upper(), stat].values[0]
    return team1value
def points_for_passing(year, team, week):
    opponent = week_opponent(year, team, week)

    return None


if __name__ == "__main__":
#    print(week_opponent(2019, 'bal', 13))
    print(compare_year('was', 'bal', 2024, 'passing'))