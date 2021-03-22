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

# Filtering data
df_selected_team = players_stats[
    (players_stats.Tm.isin(selected_team)) & (players_stats.Pos.isin(select_positon))
]
st.header("Display Player Stats of Selected Team(s)")
st.write(
    "Data dimensions: "
    + str(df_selected_team.shape[0])
    + " rows and "
    + str(df_selected_team.shape[1])
    + " columns."
)
st.dataframe(df_selected_team)

# Downloading NBA player stats data
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <=> bytes conversions
    href = f"<a href='data:file/csv;base64,{b64}' download='players_stats.csv'>Download CSV File</a>"
    return href


st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Heatmap")
    df_selected_team.to_csv("output.csv", index=False)
    df = pd.read_csv("output.csv")
    correlation = df.corr()
    mask = np.zeros_like(correlation)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(correlation, mask=mask, vmax=1, square=True)
    st.pyplot(fig)
