import streamlit as st
from ui import add_background
from pyke import Continent, Pyke, Region, Level
import requests
import pandas as pd
import plotly.express as px
import random
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key = os.environ.get("RIOT_API_KEY")

# Set the background
add_background("assets/leesin_wallpaper.png")

st.title("🔱 League of Legends Mastery Tracker")

# --- Step 1: Ask user for account info ---
col1, col2 = st.columns(2)
with col1:
    summoner_name = st.text_input("Summoner Name", "Aguscan")
with col2:
    summoner_tag = st.text_input("Tagline", "LAS")

if st.button("Get Player Data"):
    try:
        # --- Step 2: Initialize API ---
        api = Pyke(api_key)  # replace with your Riot API key

        # --- Step 3: Get champion mapping ---
        versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
        versions = requests.get(versions_url).json()
        latest_version = versions[0]

        champion_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
        champ_data = requests.get(champion_url).json()
        id_to_name = {int(v["key"]): v["name"] for v in champ_data["data"].values()}

        # --- Step 4: Get account info ---
        account = api.account.by_riot_id(Continent.AMERICAS, summoner_name, summoner_tag)
        st.markdown(f"### Player: **{account.game_name}#{account.tag_line}**")

        # --- Step 5: Get champion masteries ---
        masteries = api.champion_mastery.masteries_by_puuid(Region.LAS, account.puuid)

        mastery_data = {
            "Champion": [id_to_name[m.champion_id] for m in masteries[:10]],
            "Points": [m.champion_points for m in masteries[:10]],
        }

        st.subheader("Top 10 Champions by Mastery Points")
        df_mastery = pd.DataFrame(mastery_data)
        fig = px.pie(
            df_mastery,
            names="Champion",
            values="Points",
            title="Champion Mastery Distribution",
            color_discrete_sequence=["#FFD700", "#DAA520", "#B8860B", "#8B7500"],
        )
        fig.update_traces(textinfo="label+percent", textfont_size=14)
        st.plotly_chart(fig)

        # --- Step 6: Get a random challenge + leaderboard ---
        challenge = random.choice(api.lol_challenges.config(Region.EUW))
        top_players = api.lol_challenges.leaderboards_by_level(Region.EUW, Level.CHALLENGER, challenge.id)

        challenge_english = challenge.localized_names["en_GB"]
        st.subheader(f"Challenge: {challenge_english['name']}")
        st.write(challenge_english["description"])

        leaderboard_list = []
        for top_player in top_players[:10]:
            top_account = api.account.by_puuid(Continent.EUROPE, top_player.puuid)
            leaderboard_list.append({
                "Player": f"{top_account.game_name}#{top_account.tag_line}",
                "Rank": top_player.position,
                "Points": top_player.value,
            })

        st.subheader("Top 10 Players")
        st.table(pd.DataFrame(leaderboard_list))

    except Exception as e:
        st.error(f"❌ Error: {e}")
