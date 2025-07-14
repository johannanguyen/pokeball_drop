import pandas as pd
import os
import random
import requests

POKEMON_TRIMMED = "./assets/pokemon_trimmed.csv"
DECK = "./assets/deck.csv"
POKEMON_API = "https://pokeapi.co/api/v2/pokemon/"


def read_dataset():
    """
        Save pokemon data from dataset into a dictionary.
    """
    df = pd.read_csv(POKEMON_TRIMMED)
    df['rarity'] = pd.to_numeric(df['rarity'], errors='coerce')

    return df


def open_deck():
    """
        Open a previous deck or start an empty one.
    """
    if os.path.exists(DECK):
        df = pd.read_csv(DECK)
        deck = df.tolist(orient='records')
    else:
        deck = []
    return deck


def add_to_deck(deck, new_pokemon):
    deck.append(new_pokemon)


def pokemon_picker(df):
    """
        Use weighted probability based on rarity to pick pokemon
    """
    pulled = df.sample(n=1, weights='rarity')
    number = pulled["pokedex_number"].values[0]
    name = pulled['name'].values[0]
    type1 = pulled['type1'].values[0]
    # print(number)
    # print(name)
    # print(type1)
    print(pulled)

    response = requests.get(f"{POKEMON_API}/{number}")
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()["sprites"]["front_default"]
        print(data)

    else:
        print("Failed to fetch data", response.status_code)

df = read_dataset()
pokemon_picker(df)