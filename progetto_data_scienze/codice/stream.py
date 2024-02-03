#modo per far partire stream

# Running
#python -m streamlit run your_script.py

# is equivalent to:
#streamlit run your_script.py

import streamlit as st
import pandas as pd
import numpy as np
import time #for test and progress

#df
#final_df = pd.read_json('final_json.json')
#allprices_df = pd.read_json(
#    "C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllPrices.json"
#).T
#allcards_df = pd.read_json(
#    "C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllCards.json"
#).T
#artwork_cards_df = pd.read_json(
#    "C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/scryfall-artwork-cards.json"
#)

#2 dataframe
#normal df
#st.write("Dataframe without cleaning, 3 dataframe")
#st.write("Dataframe: ")
#st.table(allcards_df)
#st.write(allcards_df)
#clean df
#st.write("Dataframe after clean")
#st.table(final_df)

#st.write('prova')

#definizioni
#provare ad usare st.chache_data and st.cache_resource #se fatto una volta non riesegue la funzione
#@st.cache_data
#def long_running_function(param1, param2):
#    return …
#ATTENZIONE:
    #If your function is not deterministic (that is, its output depends on random numbers), 
    #or if it pulls data from an external time-varying source (for example, a live stock market ticker service) 
    #the cached value will be none-the-wiser.
@st.cache_data
def allprices_load():
    data = pd.read_json("C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllPrices.json").T
    return data

@st.cache_data
def allcards_load():
    data = pd.read_json("C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/AllCards.json").T
    return data

@st.cache_data
def artwork_cards_load():
    data = pd.read_json("C:/Users/elped/OneDrive/Documenti/hello_django/progetto_data_scienze/data_base/mtg/scryfall-artwork-cards.json")
    return data
#UI

st.title('MTG Data')

#test carico df
data_load_state = st.text('Loading data...')

allprices_df = allprices_load()
st.write(allprices_df)

allcards_df = allcards_load()
st.write(allcards_df)

artwork_cards_df = artwork_cards_load()
st.write(artwork_cards_df)

data_load_state.text('Done')

# barra progresso
#latest_iteration = st.empty()
#bar = st.progress(0)

#for i in range(100):
  # Update the progress bar with each iteration.
#  latest_iteration.text(f'Iteration {i+1}')
#  bar.progress(i + 1)
#  time.sleep(0.1)

