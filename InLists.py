import nfl_data_py as nfl


def player_in_passing(year, week, team):
    team = team.upper()

    player_names = nfl.import_weekly_data([year], columns=["week", "recent_team", "player_name", "attempts"])
    player_names = player_names[player_names["week"] == week]
    player_names = player_names[player_names["attempts"] > 0]
    player_names = player_names[player_names["recent_team"] == team]
    player_names = player_names.drop(columns=["week", "recent_team", "attempts"])
    return player_names


def player_in_rushing(year, week, team):
    team = team.upper()

    player_names = nfl.import_weekly_data([year], columns=["week", "recent_team", "player_name", "carries"])
    player_names = player_names[player_names["week"] == week]
    player_names = player_names[player_names["carries"] > 0]
    player_names = player_names[player_names["recent_team"] == team]
    player_names = player_names.drop(columns=["week", "recent_team", "carries"])
    return player_names


def player_in_receiving(year, week, team):
    team = team.upper()

    player_names = nfl.import_weekly_data([year], columns=["week", "recent_team", "player_name", "targets"])
    player_names = player_names[player_names["week"] == week]
    player_names = player_names[player_names["targets"] > 0]
    player_names = player_names[player_names["recent_team"] == team]
    player_names = player_names.drop(columns=["week", "recent_team", "targets"])
    return player_names


def player_in_sacks(year, week, team):
    team = team.upper()

    player_names = nfl.import_weekly_data([year], columns=["week", "recent_team", "player_name", "sacks"])
    player_names = player_names[player_names["week"] == week]
    player_names = player_names[player_names["sacks"] > 0]
    player_names = player_names[player_names["recent_team"] == team]
    player_names = player_names.drop(columns=["week", "recent_team", "sacks"])
    return player_names


def player_in_special(year, week, team):
    team = team.upper()

    player_names = nfl.import_weekly_data([year], columns=["week", "recent_team", "player_name", "special_teams_tds"])
    player_names = player_names[player_names["week"] == week]
    player_names = player_names[player_names["special_teams_tds"] > 0]
    player_names = player_names[player_names["recent_team"] == team]
    player_names = player_names.drop(columns=["week", "recent_team", "special_teams_tds"])
    return player_names


def player_in_passing_season(year, team):
    return None


def player_in_rushing_season(year, team):
    return None


def player_in_receiving_season(year, team):
    return None


def player_in_sacks_season(year, team):
    return None


def player_in_special_season(year, team):
    return None
