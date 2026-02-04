import nfl_data_py as nfl
import os

def player_info(year):
    print("Getting info")

    depth_charts = nfl.import_depth_charts([year])

    players = depth_charts[["gsis_id", "full_name", "club_code", "position", "depth_team"]]
    print("Data received")
    return players.drop_duplicates()

def team_schedule(year):
    data = nfl.import_schedules([year])
    teams = data[["away_team"]].drop_duplicates().sort_values("away_team").reset_index(drop =True)
    teams.index = teams.index+1
    print(teams)
    selection = input("Select team to view schedule: \n")
    selection = selection.upper()

    games = data[
        (data["home_team"] == selection) | (data["away_team"] == selection)
        ].copy()

    games["location"] = games.apply(lambda row: "HOME" if row["home_team"] == selection else "AWAY", axis =1)
    games = games.reset_index(drop = True)
    games.index = games.index +1

    schedule = games[["week", "away_team", "home_team", "location"]].to_string(index=False)
    return schedule


if __name__ == "__main__":
        user_input = input("select option: \nPlayers\nSchedules\nQuit\n\n")
        user_input = user_input.upper()

        if user_input == "PLAYERS":
            year = int(input("Enter season (2000-2024):\n"))
            players = player_info(year)

            if os.path.exists('nfl_players.xlsx'):
                os.remove('nfl_players.xlsx')
                print(f"{'nfl_players.xlsx'} existed and was deleted.")
            else:
                print(f"{'nfl_players.xlsx'} does not exist, creating new file.")

            players.to_excel('nfl_players.xlsx', index=False)
            print("File saved.")

            print("done")
        elif user_input == "SCHEDULES":
            year = int(input("Enter season (2000-2024):\n"))
            schedules = team_schedule(year)
            print(schedules)
            print("Schedule loaded")

        else:
            print("Invalid input. Please type PLAYERS, SCHEDULES, or QUIT.")
