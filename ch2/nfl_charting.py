import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import nfl_data_py as nfl
import numpy as np

seasons = range(2020, 2024 + 1)
pbp_py = nfl.import_pbp_data(seasons)

sns.set_theme(style="whitegrid", palette="colorblind")

pbp_py_comp_pass = pbp_py \
    .query('play_type == "pass" & air_yards.notnull()')\
    .reset_index()

pbp_py_comp_pass["pass_length_air_yards"] = \
    np.where(pbp_py_comp_pass["air_yards"] >= 20, "long", "short")

pbp_py_comp_pass["passing_yards"] = \
    np.where(pbp_py_comp_pass["passing_yards"].isnull(), 0, pbp_py_comp_pass["passing_yards"])

pbp_py_short_pass = pbp_py_comp_pass \
                        .query('pass_length_air_yards == "short"')

# pbp_py_hist_short = \
#     sns.displot(data=pbp_py_short_pass, binwidth=1,
#                 x="passing_yards");
# pbp_py_hist_short\
#     .set_axis_labels("Yards gained (or lost) during a passing play", "Count");

# plot of passing yards
# sns.displot(data=pbp_py, x="passing_yards")

pass_boxplot = \
    sns.boxplot(data=pbp_py_comp_pass,
                x="pass_length_air_yards",
                y="passing_yards");
pass_boxplot.set(
    xlabel="Pass Length (long >= 20 yards, short < 20 yards)",
    ylabel="Yards gained (or lost) during a passing play"
);
plt.show();