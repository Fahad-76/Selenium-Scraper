from selenium import webdriver
from selenium.webdriver.common.by import By 
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://www.premierleague.com/en/match/2561917/chelsea-vs-fulham?tab=recap")
time.sleep(3) 


scores = driver.find_elements(By.CLASS_NAME, 'match-status__score')
score_full = [s.text.strip().replace("\n", "") for s in scores]
result = "".join(score_full)
print("FullTime: " , result)

matchinfo = driver.find_elements(By.CLASS_NAME, 'scoreboard-bottom__match-info')
for m in matchinfo:
  print(m.text)

scorers = driver.find_elements(By.CLASS_NAME, 'scoreboard-event--goal')
for g in scorers:
 print(g.text)
matchstats_button = driver.find_element(By.XPATH, "//button[contains(text(),'Stats')]").click()
time.sleep(3)

stats = driver.find_elements(By.CLASS_NAME, 'match-stats__table')

known_stats = [
    "Possession", "XG", "Total Shots", "Shots On Target", "Shots Off Target",
    "Shots Inside the Box", "Shots Outside the Box", "Hit Woodwork",
    "Big Chances", "Big Chances Created", "Corners", "Saves",
    "Total Crosses (% Completed)", "Total Passes", "Long Passes (% Completed)",
    "Through Balls", "Touches", "Touches in the opposition box",
    "Tackles Won", "Blocks", "Interceptions", "Clearances",
    "Total Dribbles", "Successful Dribbles", "Duels Won",
    "Aerial Duels Won", "Distance Covered", "Red Cards", "Yellow Cards",
    "Fouls", "Offsides"
]

flat_list = []
for s in stats:
  flat_list.extend(s.text.split("\n"))

data = {"Stat": [] , "Home": [], "Away":[]}
i = 0

while i < len(flat_list):
  if flat_list[i] == "Possession":
    stat_name = flat_list[i]
    home = flat_list[i+1] if i+1 < len(flat_list) else None
    away = flat_list[i+2] if i+2 < len(flat_list) else None
    data["Stat"].append(stat_name)
    data["Home"].append(home)
    data["Away"].append(away)
    i +=3

  elif flat_list[i] in known_stats:
    stat_name = flat_list[i]
    home = flat_list[i-1] if i-1 < len(flat_list) else None
    away = flat_list[i+1] if i+1 < len(flat_list) else None
    data["Stat"].append(stat_name)
    data["Home"].append(home)
    data["Away"].append(away)

    i +=3
  else:
    i+=1

df_stats = pd.DataFrame(data)
print(df_stats)

driver.quit()
