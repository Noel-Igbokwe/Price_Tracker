import pandas as pd
import functions_temp
import datetime
import plotly.express as px

Match_df = pd.read_csv("data.csv")
PL_table = pd.read_csv('PL_table.csv').set_index("Team")

team = "Arsenal FC"

mask = False
mask = mask | (Match_df["Team1"] == team)
mask = mask | (Match_df["Team2"] == team)

Match_df = Match_df[mask].reset_index(drop=True)

dates = list(Match_df.columns)
dates.remove("Date")
dates.remove("Team1")
dates.remove("Team2")
print(dates)

dates = list(map(functions_temp.convert_string_to_date, dates))

days_until_game = []
prices = []
ratings = []

for i in range(len(Match_df)):
    dates_temp = dates
    match_date = datetime.datetime.strptime(Match_df.iat[i, 0], "%Y-%m-%d")
    for date in dates_temp:
        days_until_game.append((date - match_date).days * -1)

        team1 = Match_df.iloc[i]["Team1"]
        team2 = Match_df.iloc[i]["Team2"]

        rating1 = PL_table.loc[team1][date.strftime("%Y-%m-%d")]
        rating2 = PL_table.loc[team2][date.strftime("%Y-%m-%d")]
        rating = (rating1 + rating2) / 2
        ratings.append(rating)

    prices += list(Match_df.iloc[i].drop(["Date", "Team1", "Team2"]))

data = {"Days until game": days_until_game, "Price": prices, "Rating": ratings}
Data_df = pd.DataFrame(data=data)
fig = px.scatter_3d(Data_df,
                    x="Days until game",
                    y="Price",
                    z="Rating",
                    color=(Data_df["Rating"] * Data_df["Price"]),
                    title=(team + " ticket pricing"))

fig.show()


print(days_until_game)
print(prices)
print(ratings)
print(Match_df)
