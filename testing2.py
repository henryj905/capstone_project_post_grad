import nfl_data_py as nfl
import pandas as pd


#pd.set_option('display.max_rows',None)
data = nfl.import_schedules([2024])
print(list(data.columns))

full_data = nfl.import_sc_lines()
print(list(full_data.columns))
print(full_data[["line"]])