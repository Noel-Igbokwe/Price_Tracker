# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import selenium

import Data_Gather
import pandas as pd
import datetime
import numpy as np

try:
    # this is for the case in which this is the program's first time being run and there are no files
    # handle chrome crashing error

    data = open('data.csv', 'x')
    table = open('PL_table.csv', 'x')

    is_initialized = False

    PL_table = Data_Gather.get_table(is_initialized)
    match_df = Data_Gather.track_price(is_initialized)

    match_df.loc[match_df.astype(str).drop_duplicates().index]

    PL_table.to_csv('PL_table.csv', index=False)
    match_df.to_csv('data.csv', index=False)


except FileExistsError:
    is_initialized = True

    #empty data error!!!
    #prices in euros

    Match_df = pd.read_csv("data.csv")
    PL_table = pd.read_csv('PL_table.csv')

    PL_table[datetime.datetime.today().strftime('%Y-%m-%d')] = np.nan
    Match_df[datetime.datetime.today().strftime('%Y-%m-%d')] = np.nan

    PL_table = Data_Gather.get_table(is_initialized, PL_table)
    PL_table.to_csv('PL_table.csv', index=False)

    Match_df = Data_Gather.track_price(is_initialized, Match_df)
    Match_df.to_csv('data.csv', index=False)

    print("success")

"""
except selenium.common.exceptions.WebDriverException:
    if is_initialized == False:
        os.remove('data.csv')
        os.remove('PL_table.csv')
"""