import pandas as pd
import numpy as np
import nfl_data_py as nfl

seasons = range(2020, 2024 + 1)
pbp_py = nfl.import_pbp_data(seasons)

pbp_py_comp_pass = pbp_py \
    .query('play_type == "pass" & air_yards.notnull()')\
    .reset_index()

pbp_py_comp_pass["pass_length_air_yards"] = \
    np.where(pbp_py_comp_pass["air_yards"] >= 20, "long", "short")

pbp_py_comp_pass["passing_yards"] = \
    np.where(pbp_py_comp_pass["passing_yards"].isnull(), 0, pbp_py_comp_pass["passing_yards"])


# all passes summary
# print(pbp_py_comp_pass["passing_yards"].describe())

# short passes yard summary
# print(pbp_py_comp_pass \
#     .query('pass_length_air_yards == "short"')["passing_yards"] \
#     .describe())

# short pass epa stat description
print(pbp_py_comp_pass \
    .query('pass_length_air_yards == "short"')["epa"] \
    .describe())

# long pass epa stat description
print(pbp_py_comp_pass \
    .query('pass_length_air_yards == "long"')["epa"] \
    .describe())