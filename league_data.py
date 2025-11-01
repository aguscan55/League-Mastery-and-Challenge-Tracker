from pyke import Continent, Pyke, Region, Level
import requests
import random

api = Pyke("RGAPI-3969ee44-04f4-4bcd-bb69-944f80d55bc0")

def get_mastery_data():
    """Return account info and top 10 champion masteries."""
    versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    versions = requests.get(versions_url).json()
    latest_version = versions[0]

    champion_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
    champ_data = requests.get(champion_url).json()

    id_to_name = {
        int(info["key"]): info["name"]
        for info in champ_data["data"].values()
    }

    account = api.account.by_riot_id(Continent.AMERICAS, "Aguscan", "LAS")
    masteries = api.champion_mastery.masteries_by_puuid(Region.LAS, account.puuid)
    score = api.champion_mastery.score_by_puuid(Region.LAS, account.puuid)

    data = [
        {
            "Champion": id_to_name.get(mastery.champion_id, "Unknown"),
            "Points": mastery.champion_points,
        }
        for mastery in masteries[:10]
    ]

    return account, data, score


def get_challenge_leaderboard():
    """Return random challenge info and top 10 players."""
    challenge = random.choice(api.lol_challenges.config(Region.LAS))

    top_players = api.lol_challenges.leaderboards_by_level(
        Region.LAS, Level.CHALLENGER, challenge.id
    )

    challenge_english = challenge.localized_names["es_MX"]

    leaderboard = []
    for player in top_players[:10]:
        account = api.account.by_puuid(Continent.AMERICAS, player.puuid)
        leaderboard.append({
            "Player": f"{account.game_name}#{account.tag_line}",
            "Rank": player.position,
            "Points": player.value,
        })

    return challenge_english["name"], challenge_english["description"], leaderboard
