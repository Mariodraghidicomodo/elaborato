# all for eda

import pandas as pd
import numpy as np

#EDA AllCards
allcards_df = pd.read_json("progetto_data_scienze/codice/AllCards.json").T
allcards_df.head(5)
allcards_df.info()
allcards_df.shape
allcards_df.columns
allcards_df.isna().sum()
#allcards_df.describe()

#EDA AllPrices
allprices_df = pd.read_json("progetto_data_scienze/codice/AllPrices.json").T
allprices_df.head(5)
allprices_df.info()
allprices_df.shape
allprices_df.columns
allprices_df.isna().sum()
#allprices_df.describe()

#EDA Artwork_cards
artwork_cards_df = pd.read_json("progetto_data_scienze/codice/scryfall-artwork-cards.json")
artwork_cards_df.head(5)
artwork_cards_df.info()
artwork_cards_df.shape
artwork_cards_df.columns
artwork_cards_df.isna().sum()
#artwork_cards_df.describe()

#EDA MERGE!!!!!!!!!