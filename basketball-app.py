import base64

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.title("NBA Player Stats Explorer")

st.markdown(
    """This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)."""
)

st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox("Year", list(reversed(range(1950, 2022))))

# Web scrapping of NBA players stats
@st.cache
def load_data(year):
    url = (
        "https://www.basketball-reference.com/leagues/NBA_"
        + str(year)
        + "_per_game.html"
    )
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index)
    raw = raw.fillna(0)
    players_stats = raw.drop(["Rk"], axis=1)
    return players_stats


players_stats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(players_stats.Tm.unique())
selected_team = st.sidebar.multiselect("Team", sorted_unique_team, sorted_unique_team)

# Sidebar - Positon player selection
unique_position = ["C", "PF", "SF", "PG", "SG"]
select_positon = st.sidebar.multiselect("Position", unique_position, unique_position)
