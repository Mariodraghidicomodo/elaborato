#modo per far partire stream

# Running
#python -m streamlit run your_script.py

# is equivalent to:
#streamlit run your_script.py
#streamlit run stream.py

import streamlit as st
import pandas as pd
import numpy as np
import time #for test and progress
#from streamlit_extras.dataframe_explorer import dataframe_explorer

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

@st.cache_data
def final_load():
    data = pd.read_json("C:/Users/elped/OneDrive/Desktop/git_vs_code/prova-elab-ing/progetto_data_scienze/codice/final_json.json")
    return data

@st.cache_data
def name_cards(df):
    list_name_unique = df.name.unique()
    return list_name_unique

#serach id for image
def search_card(name,df): #rimettere apposto
    multiids = df[(df.name == name)]
    #if multiids.empty == True:
        #return ['no image',df[df.name == name].head(1)]
    #else:
        #for x in multiids.multiverse_ids:
        #    return [x[0],multiids]
    return ['no image',multiids.head(1)]

#UI

st.title('MTG Data')

#DATAFRAME!!!
st.header('Data')
final_df = final_load()
if st.checkbox('Show raw data'):
    #test carico df
    st.subheader('Raw data')
    data_load_state = st.text('Loading data...')

    st.write('Data set for prices')
    allprices_df = allprices_load()
    st.write(allprices_df)

    st.write('Data set for general information')
    allcards_df = allcards_load()
    st.write(allcards_df)

    st.write('Data set for the png and other information')
    artwork_cards_df = artwork_cards_load()
    st.write(artwork_cards_df)

    data_load_state.text('Done')

if st.checkbox('Show final data'):
    
    df = final_df
    df = df.astype(str) #devo farlo altrimneti errore conversione no image con int
    
    st.subheader('Final data')
    data_load_final_state = st.text('Loading data...')
    st.write(df) #Could not convert 'no image' with type str: tried to convert to int64, perchè in multiversid ci sono liste con int e str, quindi uso astype(str)
    data_load_final_state.text('Done')

#SEARCH IMAGE
st.header('Card')
st.subheader('Search a card')

card = st.selectbox('Insert name of the card',options=name_cards(final_df),index = 6, key='name_card') #find the multiverse_id
list_card_info = search_card(card,final_df)
#prendo image

col_img, col_info = st.columns([2, 3])
with col_img:
    if  list_card_info[0] != 'no image':
        st.image(f'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={list_card_info[0]}&type=card',use_column_width="always")
    else:
        st.write('no image found')
with col_info:
    info = list_card_info[1]
    #st.write(info[['name','released_at','layout','mana_cost','power','toughness','rarity','flavor_text','type','subtypes','text','prices']].T)
    st.dataframe(data=info[['name','released_at','layout','mana_cost','power','toughness','rarity','flavor_text','type','subtypes','text','prices']].T, use_container_width=True)

#PLOT
st.header('Plot')

#SELECT PERIOD
#with a slider
st.subheader('Select years')
start, finish = st.select_slider('Select a range', options=np.arange(1993,2019), value = (1993, 1996)) #period is a variable that i will use in the mask

#SELECT ATTRBUTE

#vedere tags
#pip install streamlit-tags

#vedere Dataframe explorer UI
#pip install streamlit-extras
#from streamlit_extras.dataframe_explorer import dataframe_explorer

#vedere multiselect

#MODEL

# barra progresso
#latest_iteration = st.empty()
#bar = st.progress(0)

#for i in range(100):
  # Update the progress bar with each iteration.
#  latest_iteration.text(f'Iteration {i+1}')
#  bar.progress(i + 1)
#  time.sleep(0.1)

