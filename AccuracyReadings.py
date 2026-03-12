import nfl_data_py as nfl
import pandas as pd

def get_results(year):
    pd.set_option('display.max_rows', None)
    results = nfl.import_schedules([year])
    results = results[['week', 'away_team', 'away_score', 'home_team', 'home_score', 'result']]
    return results


print(get_results(2024))