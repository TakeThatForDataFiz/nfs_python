import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import nfl_data_py as nfl
import numpy as np

seasons = range(2020, 2024 + 1)
pbp_py = nfl.import_pbp_data(seasons)


pbp_py_comp_pass = pbp_py.query('play_type == "pass" & air_yards.notnull()').reset_index()

pbp_py_comp_pass["pass_length_air_yards"] = \
    np.where(pbp_py_comp_pass["air_yards"] >= 20, "long", "short")


pbp_py_season = \
    pbp_py_comp_pass \
    .groupby(["passer_id", "passer", "season"]) \
    .agg({"passing_yards": ["mean", "count"]})

pbp_py_season.columns = list(map("_".join, pbp_py_season.columns.values))

pbp_py_season \
    .rename(columns={"passing_yards_mean": 'ypa',
                    'passing_yards_count': 'n'},
                    inplace=True)

# print(pbp_py_season \
#         .sort_values(by=["ypa"], ascending=False)\
#         .head(15))

pbp_py_season_100 = pbp_py_season \
                    .query("n >= 100") \
                    .sort_values(by=["ypa"], ascending=False)

# print(pbp_py_season_100.head(15))

pbp_py_p_s_pl = \
    pbp_py_comp_pass\
    .groupby(["passer_id", "passer", , "season","pass_length_air_yards"])\
    .agg({"passing_yards": ["mean", "count"]})

pbp_py_p_s_pl.columns = \
        list(map("_".join, pbp_py_p_s_pl.columns.values))
pbp_py_p_s_pl\
    .rename(columns={"passing_yards_mean": "ypa",
                    "passing_yards_count": "n"},
                    inplace=True)
pbp_py_p_s_pl.reset_index(inplace=True)

q_value = (
    '(n >= 100 and pass_length_air_yards == "short") or ' +
    '(n >= 30 and pass_length_air_yards == "long")'
)
pbp_py_p_s_pl = pbp_py_p_s_pl.query(q_value).reset_index()

cols_save = \
    ["passer_id", "passer", "season", 
    "pass_length_air_yards", "ypa"]
air_yards_py = \
    pbp_py_p_s_pl[cols_save].copy()

air_yards_lag_py = \
    air_yards_py\
    .copy()

air_yards_lag_py["season"] += 1
air_yards_lag_py \
    .rename(columns={"ypa": "ypa_last"},
            inplace=True)

pbp_py_p_s_pl = air_yards_py\
    .merge(air_yards_lag_py,
            how="inner",
            on=["passer_id", "passer", "season",
                "pass_length_air_yards"])
# print(
#     pbp_py_p_s_pl[["pass_length_air_yards", "passer",
#                     "season", "ypa", "ypa_last"]]\
#         .query('passer == "D.Maye" | passer == "A.Rodgers"')\
#         .sort_values(["passer", "pass_length_air_yards", "season"])\
#         .to_string()
# )


# sns.lmplot(data=pbp_py_p_s_pl,
#             x="ypa",
#             y="ypa_last",
#             col="pass_length_air_yards");
# plt.show();

print(pbp_py_p_s_pl \
    .query(
        'pass_length_air_yards == "long" & season == 2024'
    )[["passer_id", "passer", "ypa"]] \
    .sort_values(["ypa"], ascending=False) \
    .head(10)
)
