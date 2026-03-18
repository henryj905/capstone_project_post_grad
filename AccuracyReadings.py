import MainFile
import nfl_data_py as nfl
import pandas as pd
import Algorithm
import os
import ast


def real_results(year, team_abbr):
    data = nfl.import_schedules([year])
    teams = data[["away_team"]].drop_duplicates().sort_values("away_team")
    teams = teams.reset_index(drop=True)
    teams.index += 1
    selection = team_abbr.upper()

    games = data[(data["home_team"] == selection) | (data["away_team"] == selection)].copy()

    games["location"] = games.apply(lambda row: "HOME" if row["home_team"] == selection else "AWAY", axis=1)
    games = games.reset_index(drop=True)
    games.index = games.index+1

    schedule = games[["week", "home_team", "away_team", "result"]].copy()
    schedule["result"] = pd.to_numeric(schedule["result"])
    schedule = schedule[schedule['week'] < 19]
    winner = schedule["result"].copy()
    winner[schedule["result"] > 0] = schedule["home_team"]
    winner[schedule["result"] < 0] = schedule["away_team"]

    schedule["result"] = winner
    return schedule[['result']]


if __name__ == "__main__":
    year = 2024
    weeks = list(range(1, 19))
    stats = ["passing", "rushing", "receiving", "sacks", "special"]
    df = ''
    # for team in MainFile.teams():
    #     rows = []
    #
    #     file_name = f"{team}.csv"
    #
    #     if os.path.exists(file_name):
    #         print(f"{file_name} already exists, skipping {team}")
    #         continue
    #
    #     for week in weeks:
    #         team1stat = []
    #         team2stat = []
    #         if MainFile.return_opponent(year, team, week) == "BYE":
    #             continue
    #         for stat in stats:
    #             print(stat)
    #             team1 = Algorithm.gather_previous_weeks(team, year, week, stat)
    #             team2 = Algorithm.gather_previous_weeks(MainFile.return_opponent(year, team, week), year, week, stat)
    #             team1 = Algorithm.combine_weeks(team1)
    #             team2 = Algorithm.combine_weeks(team2)
    #             team1stat.append(team1)
    #             team2stat.append(team2)
    #
    #         team1score = 0
    #         team2score = 0
    #         for t1, t2 in zip(team1stat, team2stat):
    #             t1score, t2score = Algorithm.compare_weeks(t1, t2)
    #             team1score += t1score
    #             team2score += t2score
    #
    #         print(week)
    #
    #         team_score = team1score
    #         opponent = MainFile.return_opponent(year, team, week)
    #         opponent_score = team2score
    #         winner = Algorithm.return_winner(team, team_score, opponent, opponent_score)
    #
    #         rows.append({
    #             "team": team,
    #             "team_score": team_score,
    #             "opponent": opponent,
    #             "opponent_score": opponent_score,
    #             "predicted_winner": winner
    #         })
    #
    #         df = pd.DataFrame([rows])
    #
    #     print(df)
    #
    #     df.to_csv(
    #         file_name,
    #         mode='a',
    #         header=not os.path.exists(file_name),
    #         index=False
    #     )
    #
    #     print(f"{team} saved → {file_name}")


    for team in MainFile.teams():
        file_name = f"{team}.csv"
        for line in file_name:
            print(line)