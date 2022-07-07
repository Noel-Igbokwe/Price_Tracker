import datetime
import functions_temp as ft


def process_match_info(date, teams, prices, matches):

    date = ft.convert_date(date)
    teams = ft.convert_matchname(teams)

    matches.loc[len(matches)] = [date, teams[0], teams[1], prices]
    return matches


def update_match_price(date, teams, price, matches):

    date = ft.convert_date(date)
    teams = ft.convert_matchname(teams)
    index = matches.loc[((matches['Date'] == date.strftime('%Y-%m-%d')) & (matches['Team1'] == teams[0]) & (matches['Team2'] == teams[1]))].index

    try:
        index = index[0]
    except IndexError:
        return matches

    matches.at[index, datetime.datetime.today().strftime('%Y-%m-%d')] = price
    return matches

