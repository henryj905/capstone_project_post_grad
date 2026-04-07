import MainFile
import nfl_data_py as nfl
import pandas as pd
import os
import Algorithm
import ast
import numpy as np


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
    schedule["result"] = np.where(
        schedule["result"] > 0,
        schedule["home_team"],
        np.where(
            schedule["result"] < 0,
            schedule["away_team"],
            "TIE"
        )
    )

    return schedule[['result']]


def fix_file(file_name):
    df = pd.read_csv(file_name)

    values = df.values.flatten()
    rows = []

    for v in values:
        if not isinstance(v, str) or not v.strip():
            continue

        try:
            parsed = ast.literal_eval(v)
            if isinstance(parsed, dict):
                rows.append(parsed)
        except:
            continue

    if not rows:
        return

    clean_df = pd.DataFrame(rows)

    clean_df.to_csv(file_name, index=False)

    print(f"Fixed and overwrote {file_name}")


def get_predicted_winners(file_name):
    df = pd.read_csv(file_name)
    return df["predicted_winner"].dropna().tolist()


def run():
    years = list(range(2021, 2025))
    stats = ["passing", "rushing", "receiving", "sacks", "special"]
    df = ''
    for year in years:
        for team in MainFile.teams():
            rows = []

            file_name = f"csv_files\\{team}{year}.csv"

            if os.path.exists(file_name):
                print(f"{file_name} already exists, skipping {team}")
                continue
            print("Predicting for:", team, year)
            for week in range(1, 19):
                team1stat = []
                team2stat = []
                if MainFile.return_opponent(year, team, week) == "BYE":
                    continue
                for stat in stats:
                    team1 = Algorithm.gather_previous_weeks(team, year, week, stat)
                    team2 = Algorithm.gather_previous_weeks(MainFile.return_opponent(year, team, week),
                                                            year, week, stat)
                    team1 = Algorithm.combine(team1)
                    team2 = Algorithm.combine(team2)
                    team1stat.append(team1)
                    team2stat.append(team2)

                team1score = 0
                team2score = 0
                for t1, t2 in zip(team1stat, team2stat):
                    t1score, t2score = Algorithm.compare_weeks(t1, t2)
                    team1score += t1score
                    team2score += t2score

                print("Week", week, "complete")

                team_score = team1score
                opponent = MainFile.return_opponent(year, team, week)
                opponent_score = team2score
                winner = Algorithm.return_winner(team, team_score, opponent, opponent_score)

                rows.append({
                    "team": team,
                    "team_score": team_score,
                    "opponent": opponent,
                    "opponent_score": opponent_score,
                    "predicted_winner": winner
                })

                df = pd.DataFrame(rows)

            df.to_csv(
                file_name,
                mode='a',
                header=not os.path.exists(f"csv_files\\{file_name}"),
                index=False
            )

            print(f"{team} saved → {file_name}")
    teams = MainFile.teams()
    for year in years:
        for team in teams:
            fix_file(f"csv_files\\{team}{year}.csv")

    guesses = []
    real_result_list = []
    for year in years:
        for team in teams:
            predictions = get_predicted_winners(f"csv_files\\{team}{year}.csv")

            wins = 0
            loss = 0
            tie = 0

            for guess in predictions:
                if guess == team:
                    wins += 1
                elif guess == "TIE":
                    tie += 1
                else:
                    loss += 1

                guesses.append(guess)

            print(team, ":", wins, "-", loss, "-", tie)

    print(guesses)
    print(len(guesses))

    for year in years:
        for team in teams:
            results = real_results(year, team)

            for _, result_list in results.items():
                for x in result_list:
                    real_result_list.append(x)

    print(real_result_list)
    print(len(real_result_list))

    right = 0
    wrong = 0

    for x, y in zip(guesses, real_result_list):
        if x == y:
            right += 1
        else:
            wrong += 1

    total = right + wrong

    print("right =", right)
    print("wrong =", wrong)
    print("percentage =", round(right / total, 2))

run()
