import nfl_data_py as nfl
import os
import OffensiveStatsSeasonal
import OffensiveStatsWeekly
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
    print(teams)
    selection = team_abbr.upper()

    games = data[(data["home_team"] == selection) | (data["away_team"] == selection)].copy()

    games["location"] = games.apply(lambda row: "HOME" if row["home_team"] == selection else "AWAY", axis=1)
    games = games.reset_index(drop=True)
    games.index = games.index+1

    schedule = games[["week", "away_team", "home_team", "location"]]
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
    passing = OffensiveStatsSeasonal.passing_stats_season(year)
    rushing = OffensiveStatsSeasonal.rushing_stats_season(year)
    receiving = OffensiveStatsSeasonal.receiving_stats_season(year)
    sacks = OffensiveStatsSeasonal.sacks_by_qb_season(year)
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


if __name__ == "__main__":
    print("Season or Weekly stats?")
    question = input().upper()
    if question == "SEASON":
        print("Players    Schedules    Passing    Rushing    Receiving    Special Teams    Sacks    Depth Charts    All")
    if question == "WEEKLY":
        print("Passing    Rushing    Receiving    Sacks")
    user_input = input("select option").upper()
    user_year = int(input("Enter season (2017-2024):\n"))
    if question =="SEASON":
        if user_input == "PLAYERS":
            print(player_list(user_year))

        elif user_input == "SCHEDULES":
            print(team_schedule(user_year, 'was'))

        elif user_input == "PASSING":
            print(OffensiveStatsSeasonal.passing_stats_season(user_year))

        elif user_input == "RUSHING":
            print(OffensiveStatsSeasonal.rushing_stats_season(user_year))

        elif user_input == "RECEIVING":
            print(OffensiveStatsSeasonal.receiving_stats_season(user_year))

        elif user_input == "SPECIAL TEAMS":
            print(special_teams_tds(user_year))

        elif user_input == "SACKS":
            print(OffensiveStatsSeasonal.sacks_by_qb_season(user_year))

        elif user_input == "DEPTH CHARTS":
            team = input("Team abbreviation")
            week = int(input("Pick week (1-18): "))
            print(depth_chart(user_year, team, week))

        elif user_input == "ALL":
            print(to_excel(user_year))
        else:
            print("Invalid input. Please select from options or QUIT.")


    if question == "WEEKLY":
        week = int(input("What week (1-18): "))
        if user_input == "PASSING":
            print(OffensiveStatsWeekly.passing_weekly(user_year, week))

        elif user_input == "RUSHING":
            print(OffensiveStatsWeekly.rushing_weekly(user_year, week))

        elif user_input == "RECEIVING":
            print(OffensiveStatsWeekly.receiving_weekly(user_year, week))

        elif user_input == "SACKS":
            print(OffensiveStatsWeekly.sacks_qb_weekly(user_year, week))