import nfl_data_py as nfl
import pandas as pd

data= nfl.import_team_desc()
print(list(data.columns))
print(data[["team_abbr"]])
print(data[["team_name"]])