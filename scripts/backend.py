import pandas as pd
import requests

POKEMON_DATA = "./assets/pokemon_data.csv"
POKEMON_API = "https://pokeapi.co/api/v2/pokemon/"


def read_dataset():
    """
    Load Pokémon data from the CSV file.
    Assumes 'rarity' is used as a weight for random sampling.
    """
    df = pd.read_csv(POKEMON_DATA)
    df['rarity'] = pd.to_numeric(df['rarity'], errors='coerce')
    return df


def pokemon_picker(df):
    """
    Randomly pick a Pokémon from the dataset using rarity as weights.
    Returns the Pokémon's name and sprite URL.
    """
    pulled = df.sample(n=1, weights='rarity')
    number = pulled["pokedex_number"].values[0]
    name = pulled['name'].values[0]

    response = requests.get(f"{POKEMON_API}/{number}")
    if response.status_code == 200:
        sprite_url = response.json()["sprites"]["front_default"]
        return name.title(), sprite_url
    else:
        print(f"Could not fetch sprite - {response.status_code}")
        return name.title(), None


if __name__ == "__main__":
    df = read_dataset()
    name, sprite = pokemon_picker(df)
