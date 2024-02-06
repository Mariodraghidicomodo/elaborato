#CLEAN ALL THE DATASET

import pandas as pd
import numpy as np

#DC AllCards

allcards_df = pd.read_json("C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllCards.json").T
allcards_df_bu = allcards_df

allcards_df.drop('hasNoDeckLimit',axis=1,inplace=True)
allcards_df.drop('mtgArenaId',axis=1, inplace=True)
allcards_df.drop('mtgoId', axis = 1, inplace=True)
allcards_df.drop('mtgoFoilId',axis = 1, inplace=True)
allcards_df.drop(['B.F.M. (Big Furry Monster)'], inplace=True)
allcards_df.drop('purchaseUrls',axis=1,inplace=True)
allcards_df.drop('colorIndicator', axis = 1, inplace=True)
allcards_df.drop('hand',axis=1,inplace=True)
allcards_df.drop('life',axis = 1, inplace=True)
allcards_df.drop(['faceConvertedManaCost','names','side'], axis = 1, inplace=True)

allcards_df.isReserved.fillna('false',inplace=True)
allcards_df.text.fillna('no text', inplace=True)
allcards_df.edhrecRank.fillna('not ranked', inplace=True)
allcards_df.leadershipSkills.fillna('unusable', inplace=True)

allcards_df.loc[allcards_df[(allcards_df.name == 'Gunk Slug')].index, 'power'] = 2
allcards_df.loc[allcards_df[(allcards_df.name == 'Gunk Slug')].index, 'toughness'] = 3
allcards_df.loc[allcards_df[(allcards_df.name == 'Squidnapper')].index, 'power'] = 3
allcards_df.loc[allcards_df[(allcards_df.name == 'Squidnapper')].index, 'toughness'] = 4

#allcards_clean_df = allcards_df

#DC AllPrices
#doesn't have any null value

#DC Artwork_cards

artwork_cards_df = pd.read_json("C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/scryfall-artwork-cards.json")
artwork_cards_df_bu = artwork_cards_df

artwork_cards_df.drop(columns='tcgplayer_id', inplace=True)
artwork_cards_df.drop(columns='watermark',inplace=True)
artwork_cards_df.drop(['frame_effects','preview','promo_types','mtgo_id','color_indicator','printed_name','printed_type_line','printed_text','mtgo_foil_id','life_modifier','hand_modifier','variation_of','arena_id'], axis=1, inplace = True)

artwork_cards_df.oracle_text.fillna('No oracle text',inplace=True)
artwork_cards_df.flavor_text.fillna('No flavor text', inplace=True)
artwork_cards_df.edhrec_rank.fillna(str('not ranked'), inplace=True)
artwork_cards_df.all_parts.fillna('no combo',inplace=True)

#artwork_cards_clean_df = artwork_cards_df

#DC Merge !!!!!!!!!!!!!!!!!