import pandas as pd
import datetime as dt

def make_ranking(team_name, current_pos):
    historic_table = pd.read_csv("PL_table(historical).csv")
    index = historic_table.loc[historic_table['Team'] == team_name].index[0]

    historic_ranking = (historic_table.at[index, "2020-2021"] * 0.25) + (historic_table.at[index, "2021-2022"] * 0.75)
    td = (dt.datetime.today() - dt.datetime(2022, 8, 5)).days

    total_days = (dt.datetime(2022, 11, 12) - dt.datetime(2022, 8, 5)).days
    percent = td / total_days
    if percent > 0.75:
        percent = 0.75
    elif percent < 0:
        percent = 0
    historic_ranking = historic_ranking * (1 - percent)
    current_pos = current_pos * percent
    return historic_ranking + current_pos
