import nfl_data_py as nfl


weekly_cache = {}
seasonal_cache = {}
weekly_player_cache = {}


def player_in_passing(year, week, team):
    team = team.upper()

    if year not in weekly_cache:
        weekly_cache[year] = nfl.import_weekly_data([year])

    df = weekly_cache[year]

    df = df[
        (df["week"] == week) &
        (df["recent_team"] == team) &
        (df["attempts"] > 0)
    ]

    return df[["player_name"]]


def player_in_rushing(year, week, team):
    team = team.upper()

    if year not in weekly_cache:
        weekly_cache[year] = nfl.import_weekly_data([year])

    df = weekly_cache[year]

    df = df[
        (df["week"] == week) &
        (df["recent_team"] == team) &
        (df["carries"] > 0)
        ]

    return df[["player_name"]]


def player_in_receiving(year, week, team):
    team = team.upper()

    if year not in weekly_cache:
        weekly_cache[year] = nfl.import_weekly_data([year])

    df = weekly_cache[year]

    df = df[
        (df["week"] == week) &
        (df["recent_team"] == team) &
        (df["targets"] > 0)
        ]

    return df[["player_name"]]


def player_in_sacks(year, week, team):
    team = team.upper()

    if year not in weekly_cache:
        weekly_cache[year] = nfl.import_weekly_data([year])

    df = weekly_cache[year]

    df = df[
        (df["week"] == week) &
        (df["recent_team"] == team) &
        (df["sacks"] > 0)
        ]

    return df[["player_name"]]


def player_in_special(year, week, team):
    team = team.upper()

    if year not in weekly_cache:
        weekly_cache[year] = nfl.import_weekly_data([year])

    df = weekly_cache[year]

    df = df[
        (df["week"] == week) &
        (df["recent_team"] == team) &
        (df["special_teams_tds"] > 0)
        ]

    return df[["player_name"]]


def get_weekly_players(year):
    if year not in weekly_player_cache:
        df = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team"])
        weekly_player_cache[year] = df.drop_duplicates(subset="player_id")
    return weekly_player_cache[year]


def player_in_passing_season(year, team):
    team = team.upper()

    if year not in seasonal_cache:
        seasonal_cache[year] = nfl.import_seasonal_data([year])

    seasonal = seasonal_cache[year][["player_id", "attempts"]]
    weekly = get_weekly_players(year)

    data = seasonal.merge(weekly, on="player_id", how="left")
    data = data[(data["recent_team"] == team) & (data["attempts"] > 0)]

    return data[["player_name"]]


def player_in_rushing_season(year, team):
    team = team.upper()

    if year not in seasonal_cache:
        seasonal_cache[year] = nfl.import_seasonal_data([year])

    seasonal = seasonal_cache[year][["player_id", "carries"]]
    weekly = get_weekly_players(year)

    data = seasonal.merge(weekly, on="player_id", how="left")
    data = data[(data["recent_team"] == team) & (data["carries"] > 0)]

    return data[["player_name"]]


def player_in_receiving_season(year, team):
    team = team.upper()

    if year not in seasonal_cache:
        seasonal_cache[year] = nfl.import_seasonal_data([year])

    seasonal = seasonal_cache[year][["player_id", "targets"]]
    weekly = get_weekly_players(year)

    data = seasonal.merge(weekly, on="player_id", how="left")
    data = data[(data["recent_team"] == team) & (data["targets"] > 0)]

    return data[["player_name"]]


def player_in_sacks_season(year, team):
    team = team.upper()

    if year not in seasonal_cache:
        seasonal_cache[year] = nfl.import_seasonal_data([year])

    seasonal = seasonal_cache[year][["player_id", "sacks"]]
    weekly = get_weekly_players(year)

    data = seasonal.merge(weekly, on="player_id", how="left")
    data = data[(data["recent_team"] == team) & (data["sacks"] > 0)]

    return data[["player_name"]]


def player_in_special_season(year, team):
    team = team.upper()

    if year not in seasonal_cache:
        seasonal_cache[year] = nfl.import_seasonal_data([year])

    seasonal = seasonal_cache[year][["player_id", "special_teams_tds"]]
    weekly = get_weekly_players(year)

    data = seasonal.merge(weekly, on="player_id", how="left")
    data = data[(data["recent_team"] == team) & (data["special_teams_tds"] > 0)]

    return data[["player_name"]]
