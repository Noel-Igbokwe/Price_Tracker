import pandas
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By
import Data_Manage
import functions_temp as ft
import pandas as pd
import numpy as np
import Dynamic_Ranking as dr


def get_table(is_initialized, PL_table=pd.DataFrame(columns=['Team', datetime.datetime.today().strftime('%Y-%m-%d')])):
    ssUrl = "https://www.skysports.com/premier-league-table"
    page = requests.get(ssUrl)
    soup = BeautifulSoup(page.content, "html.parser")

    for row in soup.tbody.find_all("td", class_="standing-table__cell standing-table__cell--name"):
        team_name = row.text.strip()
        if team_name not in (
                "Manchester City", "Manchester United", "Tottenham Hotspur", "Leeds United", "Bournemouth"):
            team_name += " FC"
        elif "Bournemouth" == team_name:
            team_name = ("AFC " + team_name)
        if team_name == "Brighton and Hove Albion FC":
            team_name = "Brighton & Hove Albion FC"
        team_pos = int(row.parent.find("td", class_="standing-table__cell").text)

        if is_initialized:
            index = PL_table.loc[(PL_table['Team'] == team_name)].index[0]
            PL_table.at[index, datetime.datetime.today().strftime('%Y-%m-%d')] = dr.make_ranking(team_name, team_pos)
        else:
            a = len(PL_table)
            PL_table.at[a, 'Team'] = team_name
            PL_table.at[a, datetime.datetime.today().strftime('%Y-%m-%d')] = dr.make_ranking(team_name, team_pos)

    return PL_table


def track_price(is_initialized, matchdf=pandas.DataFrame(data=None, columns=['Date', 'Team1', 'Team2', str(datetime.datetime.today().date())])):
    chrome_path = '/usr/local/bin/chromedriver'

    stubhubUrl = "https://www.stubhub.ie/premier-league-tickets/grouping/154987/?valueMessaging=true&gclid" \
                 "=CjwKCAjw5NqVBhAjEiwAeCa97e25UG3KhjeXi4GKMK0VESe4wfaPqkncLcBirooAOldhIOAYZnOeCxoC5jsQAvD_BwE "

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(chrome_path)
    driver.get(stubhubUrl)
    time.sleep(3)

    while True:
        try:
            driver.find_element(By.XPATH, "//button[normalize-space()='See more events']").click()
            time.sleep(1)
        except:
            break

    time.sleep(3)

    elements = driver.find_elements(By.CLASS_NAME, "EventItem__Body")

    for element in elements:
        if len(element.find_element(By.CLASS_NAME, "EventItem__Details").find_elements(By.XPATH, "*")) == 2:
            price = int(ft.convert_price(element.find_element(By.CLASS_NAME, "AdvisoryPriceDisplay__content").text))
        else:
            price = np.nan

        teams = element.find_element(By.CLASS_NAME, "EventRedirection").text
        date = element.find_element(By.CLASS_NAME, "DateStamp__MonthDateYear").text

        if "VIP" in teams:
            continue

        if is_initialized:
            matchdf = Data_Manage.update_match_price(date, teams, price, matchdf)
        else:
            matchdf = Data_Manage.process_match_info(date, teams, price, matchdf)

    return matchdf
