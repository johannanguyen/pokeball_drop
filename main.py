import pandas as pd

def read_dataset():
    df = pd.read_csv('./assets/pokemon_trimmed.csv')
    print(df.head())

read_dataset()