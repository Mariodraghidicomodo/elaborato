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
import matplotlib.pyplot as plt

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
    multiids = df[(df.name == name) & (df.multiverse_ids.isin([[-1]]) == False)].head(1) #AIUTO è COME SE IL LA COLONNA MULTIIDS FOSSE DIVENTATA UNA STRINGA NON SO PERCHè, ma può essere che non ha gli scope!!??
    print(multiids.multiverse_ids)
    if multiids.empty == True:
        return ['no image',df[df.name == name].head(1)]
    else:
        for x in multiids.multiverse_ids:
            print(type(x))
            return [x[0],multiids]
    #return ['no image',multiids.head(1)]
        
def create_mask_dates(start, finish, df):
    print(start)
    print(finish)
    #mask = df['released_at'].between(start,finish)
    #oppure ritorno una lista di maskere, quindi una lista per anno, in caso potrei raggrupparli per 3 anni
    list_mask=[]
    if finish-start > 10: #raggruppo le mashere per 2 anni
        for x in range(start, finish + 1, 3):
            data_start = f'{x}-01-01'
            if x + 2 > finish: #capire, forse è inutile
                x = x+((x+2)-finish)
                data_end = f'{x}-12-31'
            else:
                data_end = f'{x+2}-12-31'
            print(data_start,data_end)
            mask = df['released_at'].between(data_start,data_end)
            list_mask.append(mask)
    else : #per anno singolo
        for x in range(start,finish + 1):
            data_start = f'{x}-01-01'
            data_end = f'{x}-12-31'
            print(data_start, data_end)
            mask = df['released_at'].between(data_start,data_end)
            list_mask.append(mask)
    return list_mask

@st.cache_data
def create_lista_all_type(df): #ok perfetto
    lista_main_type = []
    for index,tipo in df.types.items():
        for x in tipo:
            if x not in lista_main_type:
                lista_main_type.append(x)
    return lista_main_type

def search_row_by_type(search_type, df_view): #ok perfetto, ritorno gli indici che hanno il typo idicato
    lista_indici = []
    count = 0
    for index,tipo in df_view.types.items():
        #try:
            #print(search_type, tipo)
            if search_type in tipo:
                count += 1
                lista_indici.append(index)
        #except:
            #print('bro non so')
    return lista_indici


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
    
    all_str = final_df.copy() #ATTENZIONE USARE COPY SE SI VUOLE CREARE UNA COPIA DI UN dataframe
    all_str = all_str.astype(str) #devo farlo altrimneti errore conversione no image con int
    
    st.subheader('Final data')
    data_load_final_state = st.text('Loading data...')
    st.write(all_str) #Could not convert 'no image' with type str: tried to convert to int64, perchè in multiversid ci sono liste con int e str, quindi uso astype(str)
    data_load_final_state.text('Done')

#SEARCH IMAGE
st.header('Card')
st.subheader('Search a card')

card = st.selectbox('Insert name of the card',options=name_cards(final_df),index = 6, key='name_card') #find the multiverse_id
list_card_info = search_card(card,final_df)


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
start, finish = st.select_slider('Select a range', options=np.arange(1993,2019+1), value = (1993, 1996)) #period is a variable that i will use in the mask
list_mask_data = create_mask_dates(start, finish, final_df)
print(list_mask_data)

#SELECT ATTRBUTE
attribut = st.selectbox(label='Select an attribute', options=['number of card','types','general cost of mana','power','toughness','reserved'])

if attribut == 'number of card': #le date sono sbagliate perche?
    
    for x in list_mask_data:
        
        fig_nc,ax = plt.subplots(figsize=(20,6))
        df_data = final_df[x]

        ax = plt.title(f'amount of type from {df_data.released_at.min()} to {df_data.released_at.max()}')
        ax =plt.ylabel('amount')
        ax = plt.xlabel('period')
        ax = plt.bar(df_data.released_at.value_counts().index,df_data.released_at.value_counts())
        
        st.pyplot(fig_nc)
        

if attribut == 'types':
    
    lista_main_types = create_lista_all_type(final_df)
    
    for x in list_mask_data: #prima scorro le date
        
        fig, ax = plt.subplots(figsize=(15,6))
        df_data = final_df[x] #mi salvo il dataframe con la mask data
        
        list_amount_type = {} #creo dizionario per salvarmi le quantità
        
        for y in lista_main_types: #scorro i vari tipi
            amount = len(search_row_by_type(y,df_data))
            if amount > 0:
                list_amount_type[y] = amount
        
        ax = plt.bar(list_amount_type.keys(),list_amount_type.values())
        ax = plt.title(f'amount of type from {df_data.released_at.min()} to {df_data.released_at.max()}')
        ax = plt.xlabel('type of cards')
        ax = plt.ylabel('amount')
        
        st.pyplot(fig)
        
if attribut == 'general cost of mana':
    #FARNE UNO PER I COLORI NORMALI B,G,U,R,MULTI,GENERAL
    for x in list_mask_data: #prima scorro le date
        
        fig, ax = plt.subplots(figsize= (15,6))
        df_data = final_df[x] #mi salvo il dataframe con la mask data
        
        #plt.figure(figsize = (15,6)) 
        ax = plt.bar(df_data.cmc.value_counts(sort=False).index,df_data.cmc.value_counts(sort=False)) #non mi piace sortato
        ax = plt.title(f'general cost of mana from {df_data.released_at.min()} to {df_data.released_at.max()}')
        ax = plt.xlabel('general cost of mana')
        ax = plt.ylabel('amount')
        if df_data.cmc.max() > 16:
            ax = plt.xlim(-1, 16)
        else:
            ax = plt.xlim(-1, df_data.cmc.max())
        ax = plt.xticks(np.arange(0,16))
        
        st.pyplot(fig)
        #nel primi 3 anni cercano molte più carte a costo 1

if attribut == 'power':
    for x in list_mask_data: #prima scorro le date
        
        fig, ax = plt.subplots(figsize = (15,6))
        df_data = final_df[x] #mi salvo il dataframe con la mask data
        df_data = df_data[df_data.power != 'no power']
         
        ax = plt.bar(df_data.power.value_counts().index,df_data.power.value_counts()) #non mi piace sortato
        ax = plt.title(f'cards power from {df_data.released_at.min()} to {df_data.released_at.max()}')
        ax = plt.xlabel('power')
        ax = plt.ylabel('amount')
        
        st.pyplot(fig)

if attribut == 'toughness':
    for x in list_mask_data: #prima scorro le date

        fig,ax = plt.subplots(figsize = (15,6))
        df_data = final_df[x] #mi salvo il dataframe con la mask data
        df_data = df_data[df_data.toughness != 'no toughness']
        
        ax = plt.bar(df_data.toughness.value_counts().index,df_data.toughness.value_counts()) #non mi piace sortato
        ax = plt.title(f'cards power from {df_data.released_at.min()} to {df_data.released_at.max()}')
        ax = plt.xlabel('toughness')
        ax = plt.ylabel('amount')

        st.pyplot(fig)
        

#vedere tags
#pip install streamlit-tags

#vedere Dataframe explorer UI
#pip install streamlit-extras
#from streamlit_extras.dataframe_explorer import dataframe_explorer

#vedere multiselect

#OTHER PLOT

#MODEL

# barra progresso
#latest_iteration = st.empty()
#bar = st.progress(0)

#for i in range(100):
  # Update the progress bar with each iteration.
#  latest_iteration.text(f'Iteration {i+1}')
#  bar.progress(i + 1)
#  time.sleep(0.1)

