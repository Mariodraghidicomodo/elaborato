#CLEAN ALL THE DATASET

import pandas as pd
import numpy as np

#DC AllCards

allcards_df = pd.read_json("C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllCards.json").T
allcards_df_bu = allcards_df.copy()

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

allcards_clean_df = allcards_df.copy()

#DC AllPrices
allprices_df = pd.read_json("C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllPrices.json").T
allprices_df_bu = allprices_df
#doesn't have any null value

allprices_clean_df = allprices_df.copy()


#DC Artwork_cards

artwork_cards_df = pd.read_json("C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/scryfall-artwork-cards.json")
artwork_cards_df_bu = artwork_cards_df.copy()

artwork_cards_df.drop(columns='tcgplayer_id', inplace=True)
artwork_cards_df.drop(columns='watermark',inplace=True)
artwork_cards_df.drop(['frame_effects','preview','promo_types','mtgo_id','color_indicator','printed_name','printed_type_line','printed_text','mtgo_foil_id','life_modifier','hand_modifier','variation_of','arena_id'], axis=1, inplace = True)

artwork_cards_df.oracle_text.fillna('No oracle text',inplace=True)
artwork_cards_df.flavor_text.fillna('No flavor text', inplace=True)
artwork_cards_df.edhrec_rank.fillna(str('not ranked'), inplace=True)
artwork_cards_df.all_parts.fillna('no combo',inplace=True)

artwork_cards_clean_df = artwork_cards_df.copy()

#DC Merge

#merge tra i vari dataset
#merge tra scry e allcards -> oracle_id : scryfallOracleId
#merge tra allcards e prices -> uuid : index 
first_final_df = pd.merge(artwork_cards_clean_df,allcards_clean_df,left_on='oracle_id',right_on='scryfallOracleId',how='inner')
final_df = pd.merge(first_final_df,allprices_clean_df,left_on='uuid',right_on=allprices_clean_df.index, how='inner')
final_df_bu = final_df.copy()

final_df.drop(final_df[final_df.name_x != final_df.name_y].index, inplace=True)
final_df.drop('name_y',axis=1,inplace=True)
final_df.drop('layout_y',axis=1,inplace=True)
final_df.drop('power_y',axis=1,inplace=True)
final_df.drop('toughness_y',axis=1,inplace=True)
final_df.drop('colors_y',axis=1,inplace=True)
final_df.drop('legalities_y',axis=1,inplace=True)
final_df.drop('loyalty_y',axis = 1, inplace = True)
final_df.drop('manaCost',axis=1,inplace=True)
final_df.drop('convertedManaCost',axis=1,inplace=True)
final_df.drop('scryfallOracleId',axis=1,inplace=True)
final_df.drop('oracle_text',axis=1,inplace=True)
final_df.drop('type_line',axis=1,inplace=True)
final_df.drop('edhrec_rank',axis=1,inplace=True)
final_df.drop('isReserved',axis=1,inplace=True)
final_df.drop('colorIdentity',axis=1,inplace=True)
final_df.drop('card_faces',axis=1,inplace=True)
final_df.drop('foreignData', axis=1, inplace=True)

colonne_originali = final_df.columns
colonne_nuove = list(map(lambda x : x[:len(x)-2] if x[len(x)-2:] =='_x' else x , colonne_originali))
colonne_nuove
final_df.columns = colonne_nuove

final_df.reset_index(drop=True,inplace=True)

final_df.loc[final_df.power.isna() == True, 'power'] = 'no power'
final_df.loc[final_df.toughness.isna() == True, 'toughness'] = 'no toughness'
final_df.multiverse_ids = final_df.multiverse_ids.apply(lambda y: [-1] if len(y)==0 else y)
final_df.mana_cost.replace('','no mana cost',inplace = True)
final_df.colors = final_df.colors.apply(lambda y: ['no colors'] if len(y)==0 else y)
final_df.color_identity = final_df.color_identity.apply(lambda y: ['no color identity'] if len(y)==0 else y)
final_df.games = final_df.games.apply(lambda y: ['paper'] if len(y)==0 else y)
final_df.artist_ids.fillna('no artist id')
final_df.loyalty.fillna('no loyalty', inplace = True)
final_df.rulings = final_df.rulings.apply(lambda y: ['no additional rules'] if len(y)==0 else y)
final_df.subtypes = final_df.subtypes.apply(lambda y: ['no subtypes'] if len(y)==0 else y)
final_df.supertypes = final_df.supertypes.apply(lambda y: ['no supertypes'] if len(y)==0 else y)

final_clean_df = final_df.copy()
final_clean_df.to_json('final_json.json',)