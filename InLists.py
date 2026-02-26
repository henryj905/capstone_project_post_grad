import nfl_data_py as nfl

def player_in_passing(year, week, team):
    team = team.upper()

    player_names = nfl.import_weekly_data([year], columns=["week", "recent_team", "player_name", "attempts"])
    player_names = player_names[player_names["week"] == week]
    player_names = player_names[player_names["attempts"] > 0]
    player_names = player_names[player_names["recent_team"] == team]
    player_names = player_names.drop(columns = ["week", "recent_team", "attempts"])
    return player_names

def player_in_rushing(year, week, team):
    team = team.upper()

    player_names = nfl.import_weekly_data([year], columns=["week", "recent_team", "player_name", "carries"])
    player_names = player_names[player_names["week"] == week]
    player_names = player_names[player_names["carries"] > 0]
    player_names = player_names[player_names["recent_team"] == team]
    player_names = player_names.drop(columns = ["week", "recent_team", "carries"])
    return player_names