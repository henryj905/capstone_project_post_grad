import nfl_data_py as nfl
import os

import OffensivePerTeam
import playerStatsSeasonal
import playerWeeklyStats
import OffensiveTeamWeekly
import pandas as pd



def player_list(year):
    depth_charts = nfl.import_depth_charts([year])
    players = depth_charts[["gsis_id", "full_name", "club_code", "position", "depth_team"]]
    return players.drop_duplicates()


def team_schedule(year, team_abbr):
    data = nfl.import_schedules([year])
    teams = data[["away_team"]].drop_duplicates().sort_values("away_team")
    teams = teams.reset_index(drop=True)
    teams.index += 1
    selection = team_abbr.upper()

    games = data[(data["home_team"] == selection) | (data["away_team"] == selection)].copy()

    games["location"] = games.apply(lambda row: "HOME" if row["home_team"] == selection else "AWAY", axis=1)
    games = games.reset_index(drop=True)
    games.index = games.index+1

    schedule = games[["week", "home_team", "away_team", "location"]]
    return schedule


def special_teams_tds(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    total = seasonal_with_names[seasonal_with_names["special_teams_tds"] > 0]
    total = total[["player_id", "player_name", "recent_team", "special_teams_tds"]].sort_values("recent_team")
    return total


def depth_chart(year, team_abbr, week_num):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    data = nfl.import_weekly_rosters([year])

    data = data[["week", "player_id", "player_name", "team", "depth_chart_position", "status"]]
    team_abbr = team_abbr.upper()
    data = data[data["team"] == team_abbr]
    data = data[data["week"] == week_num]

    return data.sort_values(["week", "team", "depth_chart_position"]).to_string(index=False)


def to_excel(year):
    players = player_list(year)
    passing = playerStatsSeasonal.passing_stats_season(year)
    rushing = playerStatsSeasonal.rushing_stats_season(year)
    receiving = playerStatsSeasonal.receiving_stats_season(year)
    sacks = playerStatsSeasonal.sacks_by_qb_season(year)
    special = special_teams_tds(year)

    file_name = "NFL_Stats.xlsx"
    if os.path.exists(file_name):
        os.remove(file_name)

    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:

        # Write each table spaced apart horizontally
        players.to_excel(writer, sheet_name="All Stats", startrow=0, startcol=0, index=False)
        passing.to_excel(writer, sheet_name="All Stats", startrow=0, startcol=players.shape[1] + 3, index=False)

        rushing.to_excel(writer, sheet_name="All Stats", startrow=0, startcol=players.shape[1] + passing.shape[1] + 6, index=False)

        receiving.to_excel(writer, sheet_name="All Stats",
                           startrow=0,
                           startcol=players.shape[1] + passing.shape[1] + rushing.shape[1] + 9,
                           index=False)

        sacks.to_excel(writer, sheet_name="All Stats",
                       startrow=0,
                       startcol=players.shape[1] + passing.shape[1] + rushing.shape[1] + receiving.shape[1] + 12,
                       index=False)

        special.to_excel(writer, sheet_name="All Stats",
                         startrow=0,
                         startcol=players.shape[1] + passing.shape[1] + rushing.shape[1] +
                                  receiving.shape[1] + sacks.shape[1] + 15,
                         index=False)
    worksheet = writer.sheets["All Stats"]

    for column_cells in worksheet.columns:
        max_length = 0
        column = column_cells[0].column_letter  # Get column letter

        for cell in column_cells:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        adjusted_width = max_length + 2
        worksheet.column_dimensions[column].width = adjusted_width

    print("NFL_Stats.xlsx created successfully.")

def teams():
    abbr = nfl.import_team_desc()
    abbr = abbr[["team_abbr", "team_name"]]

    teams_to_remove = ["LA", "SD", "OAK" , "STL"]

    data = abbr[~abbr["team_abbr"].isin(teams_to_remove)]

    return data["team_abbr"].tolist()


if __name__ == "__main__":
    print(teams())
    print("Season, Weekly, Season Totals, or Weekly Totals?")
    question = input().upper()

    if question == "SEASON":
        print("Players    Schedules    Passing    Rushing    Receiving    Special Teams    Sacks    Depth Charts    All")
    elif question == "WEEKLY" or question == "SEASON TOTALS" or question == "WEEKLY TOTALS":
        print("Passing    Rushing    Receiving    Sacks")

    user_input = input("select option").upper()
    user_year = int(input("Enter season (2017-2024):\n"))

    if question == "SEASON":
        season_functions = {
            "PLAYERS": lambda: print(player_list(user_year)),
            "SCHEDULES": lambda: print(team_schedule(
                user_year,
                input("Team abbreviation: ").upper()
            )),
            "PASSING": lambda: print(playerStatsSeasonal.passing_stats_season(user_year)),
            "RUSHING": lambda: print(playerStatsSeasonal.rushing_stats_season(user_year)),
            "RECEIVING": lambda: print(playerStatsSeasonal.receiving_stats_season(user_year)),
            "SPECIAL TEAMS": lambda: print(special_teams_tds(user_year)),
            "SACKS": lambda: print(playerStatsSeasonal.sacks_by_qb_season(user_year)),
            "DEPTH CHARTS": lambda: print(depth_chart(
                user_year,
                input("Team abbreviation: ").upper(),
                int(input("Pick week (1-18): "))
            )),
            "ALL": lambda: print(to_excel(user_year))
        }

        func = season_functions.get(user_input.upper())
        if func:
            func()
        else:
            print("Invalid input. Please select from options or QUIT.")

    elif question == "WEEKLY":
        week = int(input("What week (1-18): "))

        stat_functions = {
            "PASSING": playerWeeklyStats.passing_weekly,
            "RUSHING": playerWeeklyStats.rushing_weekly,
            "RECEIVING": playerWeeklyStats.receiving_weekly,
            "SACKS": playerWeeklyStats.sacks_qb_weekly
        }

        func = stat_functions.get(user_input)
        if func:
            print(func(user_year, week))
        else:
            print("Invalid input. Choose PASSING, RUSHING, RECEIVING, or SACKS.")

    elif question == "SEASON TOTALS":
        stat_functions = {
            "PASSING": OffensivePerTeam.team_passing_season,
            "RUSHING": OffensivePerTeam.team_rushing_season,
            "RECEIVING": OffensivePerTeam.team_receiving_season,
            "SACKS": OffensivePerTeam.team_sacks_season
        }

        func = stat_functions.get(user_input)
        if func:
            print(func(user_year))
        else:
            print("Invalid input. Choose PASSING, RUSHING, RECEIVING, or SACKS.")

    elif question == "WEEKLY TOTALS":
        user_team = input("What team (abbreviation): ").upper()
        while user_team not in teams():
            user_team = input("What team (abbreviation): ").upper()
        user_week = int(input("Enter week to view week by week data: "))
        print(OffensiveTeamWeekly.team_weekly_stats(user_team, user_year, user_week, user_input))