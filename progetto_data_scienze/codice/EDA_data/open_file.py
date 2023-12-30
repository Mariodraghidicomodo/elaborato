import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# path
percorso = "C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/"

# AllPrices
allprices_df = pd.read_json(
    "C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllPrices.json"
).T
# AllCards
allcards_df = pd.read_json(
    "C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllCards.json"
).T

# scryfall-artwork-cards
artwork_cards_df = pd.read_json(
    "C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/scryfall-artwork-cards.json"
)
artwork_cards_df_bu = artwork_cards_df

# AllPrintings
allprintings_df = pd.read_json(percorso + "AllPrintings.json").T
