# Capstone Project - NFL Game Prediction System

## Getting Started

This project is a data-driven NFL game prediction system that uses historical player and team statistics to predict game outcomes and evaluate accuracy.

---

## Setup

1. Navigate to the project folder:
cd capstone_project

2. Install dependencies:
pip install nfl_data_py pandas numpy kivy

3. Run the program:
python UI.py

---

## Project Overview

### Description
This system predicts NFL game outcomes using:
- Player-level weekly statistics
- Seasonal performance data
- A custom scoring algorithm

Predictions are generated for each team and compared against real results to calculate accuracy.

---

## Features

- Predicts winners for all NFL weeks (1–18)
- Uses multiple stat categories:
  - Passing
  - Rushing
  - Receiving
  - Sacks
  - Special Teams
- Aggregates previous weeks' performance
- Outputs predictions to CSV files
- Calculates overall accuracy
- Includes UI for player stats and predictions

---

## Project Structure

AccuracyReadings.py     - Runs predictions and accuracy  
Algorithm.py            - Scoring and comparison logic  
Gathers.py              - Collects player/team stats  
InLists.py              - Filters players by stat  
MainFile.py             - Schedules and opponents  
playerWeeklyStats.py    - Weekly player data  
playerStatsSeasonal.py  - Seasonal player data  
PredictorUI.py          - Prediction UI  
PlayerStatsUI.py        - Player stats UI  
csv_files/              - Output CSV files  
Logos/                  - Team logos  

---

## Usage

Run the main script:

python UI.py

Output:
- UI will display, click through desired path

Testing Accuracy

Run AccuracyReadings.py

Output:
- {team}{year}.csv files
- guesses right/wrong, accuracy percentage

---

## Future Improvements

- Improve scoring algorithm
- Add machine learning model
- Optimize performance
- Enhance UI design
- Add visualizations
- Add defensive stats
- Weather implications
- Better injury reader

---

## Author

Henry Johnson

---

## License

This project is for educational use.

---

## Project Status

Active development (Capstone Project)