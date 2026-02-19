import OffensiveStatsWeekly
import MainFile

def week_by_week_passing(team, year, week, stat):
    stat = stat.upper()
    team = team.upper()
    options = {
        "PASSING": OffensiveStatsWeekly.passing_weekly(year, week),
        "RUSHING": OffensiveStatsWeekly.rushing_weekly(year, week),
        "RECEIVING": OffensiveStatsWeekly.receiving_weekly(year, week),
        "SACKS": OffensiveStatsWeekly.sacks_qb_weekly(year, week)
    }

    if team not in MainFile.teams():
        return f"Use team abbreviations"
    if year < 2017:
        return f"Year not in allowed range (2017 - 2024)"
    if week < 0:
        return f"Week invalid, cannot be negative"
    if stat not in options :
        return f"stat not in options: {options}"
    if week == 1:
        return

    return

print(week_by_week_passing('was', 2024, 1, 'passing'))