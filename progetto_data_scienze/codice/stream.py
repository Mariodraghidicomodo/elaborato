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
import seaborn as sb
from wordcloud import WordCloud
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import warnings
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import plotly.express as px


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
    data = pd.read_json("AllPrices.json").T
    return data

@st.cache_data
def allcards_load():
    data = pd.read_json("AllCards.json").T
    return data

@st.cache_data
def artwork_cards_load():
    data = pd.read_json("scryfall-artwork-cards.json")
    return data

@st.cache_data
def final_load():
    data = pd.read_json("final_json.json")
    return data

#@st.cache_data
#def name_cards(df): # PROVARE A PASSARLE TUTTE, INSIEME ALL'ACRONIMO DEL SET
#    list_name_unique = df.name.unique()
#    list_name_unique = df[['name','set_name']]
#    print(list_name_unique)
#    return list_name_unique

#SEACH WITH SET
#def name_cards(df):
#    list_name = df[['name','set_name']]
#    list_select_card = []
#    for x in list_name:
#        #list_select_card = []
#        stringa = x.name + ' set: ' + x.set_name
#        list_select_card.append(stringa)

@st.cache_data
def name_cards(df): # PROVARE A PASSARLE TUTTE, INSIEME ALL'ACRONIMO DEL SET
    list_name_unique = df.name.unique()
    #list_name_unique = df[['name','set_name']]
    print(list_name_unique)
    return list_name_unique


#SEARCH 2 id for image AND SET
#def search_card(name,df): #rimettere apposto
#    multiids = df[(df.name == name) & (df.multiverse_ids.isin([[-1]]) == False)].head(1) #AIUTO è COME SE IL LA COLONNA MULTIIDS FOSSE DIVENTATA UNA STRINGA NON SO PERCHè, ma può essere che non ha gli scope!!??
#    print(multiids.multiverse_ids)
#    if multiids.empty == True:
#        return ['no image',df[df.name == name].head(1)]
#    else:
#        for x in multiids.multiverse_ids:
#            print(type(x))
#            return [x[0],multiids]
#    #return ['no image',multiids.head(1)]

#search id for image
def search_card(name,df): #rimettere apposto
    multiids = df[(df.name == name) & (df.multiverse_ids.isin([[-1]]) == False)].head(1)
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

@st.cache_data #testare con e senza cache
def create_lista_all_type(df): #ok perfetto
    lista_main_type = []
    for index,tipo in df.types.items():
        for x in tipo:
            if x not in lista_main_type:
                lista_main_type.append(x)
    return lista_main_type

def create_lista_subtypes(df): #ok perfetto
    lista_subtypes = []
    for index,tipo in df.subtypes.items():
        for x in tipo:
            if (x not in lista_subtypes) & (x != 'no subtypes'):
                lista_subtypes.append(x)
    return lista_subtypes

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

def search_row_by_subtypes(search_type, df_view):
    lista_indici = []
    count = 0
    for index,tipo in df_view.subtypes.items():
        #try:
            #print(search_type, tipo)
            if search_type in tipo:
                count += 1
                lista_indici.append(index)
        #except:
            #print('bro non so')
    #return lista_indici
    return count

def count_color_identity(df_search): #futur add dataframe 
    dizi_coloridentiti =  {'Black':0,'White':0,'Green':0,'Red':0,'Blue':0,'Colorless':0,'Multicolor':0}
    for x in df_search.color_identity: #x is a list
        #print(x)
        if len(x) > 1:
            dizi_coloridentiti['Multicolor'] += 1
        #elif len(x) == 0: #attenzione non ho modificato color identity, se non ha nulla posso mettere un acronimo : CL
        #    dizi_coloridentiti['Colorless'] += 1
        else:  #len == 1
            if x[0] == 'B':
                dizi_coloridentiti['Black'] += 1
            elif x[0] == 'W':
                dizi_coloridentiti['White'] += 1
            elif x[0] == 'G':
                dizi_coloridentiti['Green'] += 1
            elif x[0] == 'R':
                dizi_coloridentiti['Red'] += 1
            elif x[0] == 'U' :
                dizi_coloridentiti['Blue'] += 1
            else: #'no color identity'
                dizi_coloridentiti['Colorless'] +=1
    return dizi_coloridentiti

def count_legal_cards(df):
    lista_formats = {'standard':0,'future':0,'historic':0,'pioneer':0,'modern':0,'legacy':0,'pauper':0,'vintage':0,'penny':0,'commander':0,'brawl':0,'duel':0,'oldschool':0} #conto solo quelle legali, differenza -> non legali
    for indice,dict_legale in df.legalities.items():
        #count += 1
        #print(count)
        #print(type(legale))
        for forma,legal in dict_legale.items(): #scorro il dizionario
            #print(f)
            if forma in lista_formats:
                if legal == 'legal':
                    lista_formats[forma] += 1
    return lista_formats



#def count_subtypes(search_subtype): #ok perfetto, lo modifico e ritorno un count, non posso la lista la devo ritrasformare in un dizio
#    lista_indici = []
#    count = 0
#    for index,tipo in final_clean_df.subtypes.items():
#        if search_subtype in tipo:
#            count += 1
#            lista_indici.append(index)
#    return count

#def color_type(type):
#    for tipo in type.keys:
#        print(tipo)
#    return #DA FINIRE



#UI

st.title('MTG Data')
st.image(image='logo_magic.png', width=550)

st.markdown("""Magic The Gathering (MTG, or just Magic) is a trading card game first published in 1993 by Wizards of the Coast. This game has seen immense popularity and new cards are still released every few months. The strength of different cards in the game can vary wildly and as a result some cards now sell on secondary markets for as high as thousands of dollars.""")
st.markdown("""Link datasets: https://www.kaggle.com/datasets/mylesoneill/magic-the-gathering-cards/""")

#DATAFRAME!!!
st.header('Data')

st.markdown("""The final dataset is a collection of all cards printed from 1993 to 2019. Three datasets were utilized: one containing information about individual cards, another for card prices during the 2019 period, and a third containing additional information such as an ID for card visualization.""")

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
    
    if st.checkbox('Columns information'):
        st.markdown("""
                    id: Unique identifier of the card.\n 
                    oracle_id: A unique ID for this card’s oracle identity. This value is consistent across reprinted card editions, and unique among different cards with the same name.\n
                    multiverse_ids: Code to display card images; if it is equal to -1, the image is not available.\n
                    name: Name of the card.\n
                    lang: The language of the card.\n
                    released_at: When the card was published.\n
                    layout: The layout property categorizes the arrangement of card parts, faces, and other bounded regions on cards. The layout can be used to programmatically determine which other properties on a card you can expect.\n
                    highres_image: If there is a high-resolution image available.\n
                    mana_cost: Specifies how much and what type of mana needs to spend to play the card.\n
                    cmc: Specifies how much mana needs to spend to play the card without the type of mana.\n
                    power: The strength of the card, a key attribute for creature-type cards.\n
                    toughness: The constitution of the card, a key characteristic for creature-type cards.\n
                    colors: List of type of mana present in the mana_cost.\n
                    color_identity: List of type of mana present in the mana cost and in the text box.\n
                    legalities: In what format the card is playable or not.\n
                    games: A list of games that this card print is available in, paper, arena, and/or mtgo.\n
                    reserved: Whether there is a possibility that the card will be reprinted or not.\n
                    foil: If there is a foil version of the card.\n
                    nonfoil: If there is a foil version of the card.\n
                    oversize: True if this card is oversized.\n
                    promo: True if this card is a promotional print.\n
                    reprint: If the card was reprinted.\n
                    variation: Whether this card is a variation of another printing.\n
                    set: Set_name code.\n
                    set_name: The name of the set where the card is present.\n
                    set_type: Type of the set.\n
                    collector_number: This card’s collector number.\n
                    digital: True if this card was only released in a video game.\n
                    rarity: The rarity of the card, indicating how likely it is to be found. \n
                    flavor_text: Flavor text is always the bottom-most and italicized in the text box and has no functionality on the cards except during acorn games.\n
                    artist: The name of the artist who illustrated the card.\n
                    border_color: This card’s border color: black, white, borderless, silver, or gold.\n
                    frame: General appearance of the card.\n
                    full_art: True if this card’s artwork is larger than normal.\n
                    textless: True if the card is printed without text.\n
                    booster: Whether this card is found in boosters.\n
                    story_spotlight: True if this card is a Story Spotlight.\n
                    all_parts: All the cards needed to perform a combo.\n
                    loyalty: Statistics for the card type 'Planeswalker,' indicated in the text with a number in curly brackets and is a type of counter.\n
                    printings: In which other sets the card has been printed.\n
                    rulings: Additional rules of the card.\n
                    subtypes: Subtype is just a method of categorization with no rules specific to them, though other cards may refer to subtypes or are dependent on subtypes.\n
                    supertypes: Supertype gives additional game rules for the card.\n
                    text: Contains all relvant rules text as well all possible flavor text.\n
                    type: To the left of the center box of the card is the card type, possibly preceded by one or more supertype and/or followed by one or more supertypes. The type specifies when and how a card can be played.\n
                    types: List of all type of the card.\n
                    uuid: Universal unique identifier for the name of the card.\n
                    edhrecRank: This card’s overall rank/popularity on EDHREC. Not all cards are ranked.\n
                    leadershipSkills: The Leadership Skills Data Model describes the properties of formats that a card is legal to be your Commander in play formats that utilize Commanders.\n
                    prices: An object containing daily price information for this card.\n""")

#SEARCH IMAGE
st.header('Card')
st.subheader('Search a card')

st.markdown("""With this tool, you can search for the name of a card. On the left, the card's image will be displayed, while on the right, a set of important card details will be shown.""")

card = st.selectbox('Insert name of the card',options=name_cards(final_df),index = 6, key='name_card') #find the multiverse_id
#card = st.selectbox('Insert name of the card',options=list_select_card,index = 6, key='name_card') #find the multiverse_id
#print('card:',card )
list_card_info = search_card(card,final_df) #PROVARE A MODIFICARE


col_img, col_info = st.columns([2, 3])
with col_img:
    if  list_card_info[0] != 'no image':
        
        st.image(f'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={list_card_info[0]}&type=card',use_column_width="always")
    else:
        #st.write('no image found')
        st.image(image = 'no_image.jpg', use_column_width=True)
with col_info:
    info = list_card_info[1]
    #st.write(info[['name','released_at','layout','mana_cost','power','toughness','rarity','flavor_text','type','subtypes','text','prices']].T)
    st.dataframe(data=info[['name','released_at','layout','mana_cost','power','toughness','rarity','flavor_text','type','subtypes','text','prices','uuid']].T, use_container_width=True)

#AGGIUNGERE UN SEARCH IMAGE AVANZATO

st.header('Correlation')

if st.checkbox('Show correlation'):
    fig,ax = plt.subplots()
    ax = sb.heatmap(final_df.corr(numeric_only=True),annot=True, fmt=".1f", linewidth=.5, cmap='Greens')
    st.pyplot(fig)
    st.markdown("""Observing the image, we can conclude that some variables are highly correlated both positively and negatively, such as nonfoil and booster, promo and nonfoil, or highers_image and digital. I have decided not to represent them with a plot because, being all boolean variables, i am unsure how to interpret them""")

#PLOT
st.header('Plot')

#if st.checkbox('Show correlation'):
    #fig,ax = plt.subplots()
    #ax = sb.heatmap(final_df.corr(numeric_only=True),annot=True, fmt=".1f", linewidth=.5)
    #st.pyplot(fig)


#SELECT PERIOD
#with a slider
#st.subheader('Select years')

st.markdown("""To visualize the graphs, you need to choose two variables. The first involves selecting the release period of the cards, while the second involves choosing a variable related to the cards. The final result will often be a graph depicting the quantity of cards with the selected variable over the chosen period of time""")

start, finish = st.select_slider('Select a range', options=np.arange(1993,2019+1), value = (1993, 1996)) #period is a variable that i will use in the mask
list_mask_data = create_mask_dates(start, finish, final_df)
print(list_mask_data)

#SELECT ATTRBUTE
attribut = st.selectbox(label='Select an attribute', options=['number of card','types','general cost of mana','color identity','power','toughness','reserved','legalities','subtypes','text','artist'])

if attribut == 'number of card':
    
    for x in list_mask_data:
        
        #fig_nc,ax = plt.subplots(figsize=(20,6))
        fig_nc,ax = plt.subplots(figsize=(15,6))
        
        df_data = final_df[x]

        if(finish-start > 10):
            ax = plt.title(f'Amount of cards from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            ax = plt.title(f'Amount of cards from {str(df_data.released_at.min())[0:4]}')
        ax =plt.ylabel('Amount')
        ax = plt.xlabel('Period')
        #ax = plt.bar(df_data.released_at.value_counts().index,df_data.released_at.value_counts(), width=3)
        
        order_pr = df_data.released_at.value_counts().sort_index()
        
        ax = sb.barplot(x = order_pr.index, y = order_pr)
        for x in ax.containers:
            ax.bar_label(x,)
        
        ax.tick_params(rotation = 90)

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
        
        #ax = plt.bar(list_amount_type.keys(),list_amount_type.values(),color=color_type(list_amount_type))
        #ax = sb.barplot(list_amount_type, x="keys", y="values", hue="keys")
        print(list_amount_type)
        ax = sb.barplot(x=list(list_amount_type.keys()), y=list_amount_type.values(), hue=list(list_amount_type.keys()), hue_order=lista_main_types)
        
        for x in ax.containers:
            ax.bar_label(x,)

        if(finish-start > 10):
            ax = plt.title(f'Amount of type from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            ax = plt.title(f'Amount of type from {str(df_data.released_at.min())[0:4]}')
        ax = plt.xlabel('Type of cards')
        ax = plt.ylabel('Amount')
        
        st.pyplot(fig)
    
    total = st.checkbox('Total')

    if total:

        fig,ax = plt.subplots(figsize = (20,6))
        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask]

        list_amount_type = {}

        for y in lista_main_types: #scorro i vari tipi
            amount = len(search_row_by_type(y,df_data))
            if amount > 0:
                list_amount_type[y] = amount
        
        #ax = plt.bar(list_amount_type.keys(),list_amount_type.values())
        ax = sb.barplot(x=list(list_amount_type.keys()), y=list_amount_type.values(), hue=list(list_amount_type.keys()), hue_order=lista_main_types)

        for x in ax.containers:
            ax.bar_label(x,)

        if(finish != start):
            ax = plt.title(f'Amount of type from {start} to {finish}')
        else:
            ax = plt.title(f'Amount of type from {start}')
        ax = plt.xlabel('Type of cards')
        ax = plt.ylabel('Amount')

        st.pyplot(fig)

if attribut == 'general cost of mana': #fare curva di mana (normal distribution)
    #FARNE UNO PER I COLORI NORMALI B,G,U,R,MULTI,GENERAL
    for x in list_mask_data: #prima scorro le date
        
        #fig, ax = plt.subplots(figsize= (15,6))
        df_data = final_df[x & (final_df.cmc != 1000000.0)] #mi salvo il dataframe con la mask data
        
        prova_ge= df_data.cmc.value_counts().sort_index()
        #print(prova_ge.sort_index())

        #ax = plt.bar(df_data.cmc.value_counts(sort=False).index,df_data.cmc.value_counts(sort=False)) #non mi piace sortato
        fig_px = px.line(x = prova_ge.index, y = prova_ge, labels = {'x':'Cost of mana', 'y':'Amount'})
        #ax = sb.histplot(data = df_data, x = df_data.cmc, kde=True, color='Green') #lento e ha problemi
        #ax = sb.histplot(data = df_data, x = df_data.cmc, kde=True, color='Green', stat='count', discrete=True, hue="set_name")

        if(finish - start > 10):
            #ax = plt.title(f'General cost of mana from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
            fig_px.update_layout(title = f'General cost of mana from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            #ax = plt.title(f'General cost of mana from {str(df_data.released_at.min())[0:4]}')
            fig_px.update_layout(title = f'General cost of mana from {str(df_data.released_at.min())[0:4]}')
        #ax = plt.xlabel('General cost of mana')
        #ax = plt.ylabel('Amount')

        #if df_data.cmc.max() > 16:
        #    ax = plt.xlim(-1, 16)
        #else:
        #    ax = plt.xlim(-1, df_data.cmc.max())
        #ax = plt.xticks(np.arange(0,16))
        
        #st.pyplot(fig)
        st.write(fig_px)

    total = st.checkbox('Total')

    if total:

        #fig,ax = plt.subplots(figsize=(15,6))
        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask & (final_df.cmc != 1000000.0)]

        prova_ge= df_data.cmc.value_counts().sort_index()

        #ax = plt.bar(df_data.cmc.value_counts(sort=False).index,df_data.cmc.value_counts(sort=False)) #non mi piace sortato
        fig_px = px.line(x = prova_ge.index, y = prova_ge, labels = {'x':'Cost of mana', 'y':'Amount'})

        if(finish != start):
            #ax = plt.title(f'General cost of mana from {start} to {finish}')
            fig_px.update_layout(title = f'General cost of mana from {start} to {finish}')
        else:
            #ax = plt.title(f'General cost of mana from {start}')
            fig_px.update_layout(title = f'General cost of mana from {start}')

        #ax = plt.xlabel('General cost of mana')
        #ax = plt.ylabel('Amount')

        #if df_data.cmc.max() > 16:
        #    ax = plt.xlim(-1, 16)
        #else:
        #    ax = plt.xlim(-1, df_data.cmc.max())
        #ax = plt.xticks(np.arange(0,16))
        
        #st.pyplot(fig)
        st.write(fig_px)
        

if attribut == 'power':
    for x in list_mask_data: #prima scorro le date
        
        fig, ax = plt.subplots(figsize = (15,6))
        df_data = final_df[x] #mi salvo il dataframe con la mask data
        df_data = df_data[df_data.power != 'no power']
         
        #ax = plt.bar(df_data.power.value_counts().index,df_data.power.value_counts()) #non mi piace sortato
        ax = sb.barplot(x=df_data.power.value_counts().index, y=df_data.power.value_counts())
        for x in ax.containers:
            ax.bar_label(x,)

        if(finish - start > 10):
            ax = plt.title(f'Cards power from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            ax = plt.title(f'Cards power from {str(df_data.released_at.min())[0:4]}')
        ax = plt.xlabel('Power')
        ax = plt.ylabel('Amount')
        
        st.pyplot(fig)
    
    total = st.checkbox('Total')

    if total:

        fig,ax = plt.subplots(figsize = (15,6))
        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask]
        df_data = df_data[df_data.power != 'no power']

        #ax = plt.bar(df_data.power.value_counts().index,df_data.power.value_counts()) #non mi piace sortato
        ax = sb.barplot(x=df_data.power.value_counts().index, y=df_data.power.value_counts())
        for x in ax.containers:
            ax.bar_label(x,)

        if(finish != start):
            ax = plt.title(f'Cards power from {start} to {finish}')
        else:
            ax = plt.title(f'Cards power from {start}')
        ax = plt.xlabel('Power')
        ax = plt.ylabel('Amount')
        
        st.pyplot(fig)

if attribut == 'toughness':
    for x in list_mask_data: #prima scorro le date

        fig,ax = plt.subplots(figsize = (15,6))
        df_data = final_df[x] #mi salvo il dataframe con la mask data
        df_data = df_data[df_data.toughness != 'no toughness']
        
        #ax = plt.bar(df_data.toughness.value_counts().index,df_data.toughness.value_counts()) #non mi piace sortato
        ax = sb.barplot(x=df_data.toughness.value_counts().index, y=df_data.toughness.value_counts())
        for x in ax.containers:
            ax.bar_label(x,)

        if(finish -start > 10):
            ax = plt.title(f'Cards toughness from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            ax = plt.title(f'Cards toughness from {str(df_data.released_at.min())[0:4]}')
        ax = plt.xlabel('Toughness')
        ax = plt.ylabel('Amount')

        st.pyplot(fig)
    
    total = st.checkbox('Total')

    if total: 

        fig,ax = plt.subplots(figsize = (15,6))
        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask]
        df_data = df_data[df_data.toughness != 'no toughness']

        #ax = plt.bar(df_data.toughness.value_counts().index,df_data.toughness.value_counts()) #non mi piace sortato
        ax = sb.barplot(x=df_data.toughness.value_counts().index, y=df_data.toughness.value_counts())
        for x in ax.containers:
            ax.bar_label(x,)

        if(finish != start):
            ax = plt.title(f'Cards toughness from {start} to {finish}')
        else:
            ax = plt.title(f'Cards toughness from {start}')
        ax = plt.xlabel('Toughness')
        ax = plt.ylabel('Amount')

        st.pyplot(fig)


if attribut == 'reserved':
    #diviso per periodo, carte reserved
    for x in list_mask_data: #prima scorro le date
        
        #fig,ax = plt.subplots(figsize = (4,4))
        df_data = final_df[x] #mi salvo il dataframe con la mask data
        fig_px = px.pie(values = df_data.reserved.value_counts(), names = df_data.reserved.value_counts().index)

        #plt.bar(df_data.reserved.value_counts().index,df_data.reserved.value_counts()) #non mi piace sortato
        #if True in df_data.reserved.value_counts().index:
            #ax = plt.pie(df_data.reserved.value_counts(),labels=df_data.reserved.value_counts().index,explode=(0,0.5), autopct='%1.2f%%', colors=['red', 'green']) #non posso usare explod nel caso non sia presente un true
        #else:
            #ax = plt.pie(df_data.reserved.value_counts(),labels=df_data.reserved.value_counts().index, autopct='%1.2f%%', colors='red') #non posso usare explod nel caso non sia presente un true
        
        if(finish - start > 10):
            #ax = plt.title(f'Percentage of reserved cards from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
            fig_px.update_layout(title = f'Percentage of reserved cards from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            #ax = plt.title(f'Percentage of reserved cards from {str(df_data.released_at.min())[0:4]}')
            fig_px.update_layout(title = f'Percentage of reserved cards from {str(df_data.released_at.min())[0:4]}')

        #st.pyplot(fig)
        st.write(fig_px)
    
    total = st.checkbox('Total')

    if total:

        #fig,ax = plt.subplots(figsize = (4,4))
        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask]
        fig_px = px.pie(values = df_data.reserved.value_counts(), names = df_data.reserved.value_counts().index)

        #plt.bar(df_data.reserved.value_counts().index,df_data.reserved.value_counts()) #non mi piace sortato
        #if True in df_data.reserved.value_counts().index:
            #ax = plt.pie(df_data.reserved.value_counts(),labels=df_data.reserved.value_counts().index,explode=(0,0.5), autopct='%1.2f%%', colors=['red', 'green']) #non posso usare explod nel caso non sia presente un true
        #else:
            #ax = plt.pie(df_data.reserved.value_counts(),labels=df_data.reserved.value_counts().index, autopct='%1.2f%%', colors='red') #non posso usare explod nel caso non sia presente un true
        
        if(finish != start):
            #ax = plt.title(f'Percentage of reserved cards from {start} to {finish}')
            fig_px.update_layout(title = f'Percentage of reserved cards from {start} to {finish}')
        else:
            #ax = plt.title(f'Percentage of reserved cards from {start}')
            fig_px.update_layout(title = f'Percentage of reserved cards from {start}')

        #st.pyplot(fig)
        st.write(fig_px)


if attribut == 'color identity': #fare la stessa cosa con COLORS
    
    color_cid = {'Green':'green','Red':'red','Blue':'blu','Black':'black','White':'yellow','Multicolor':'orange','Colorless':'gray'}

    for x in list_mask_data:
        
        #fig,ax = plt.subplots(figsize = (15,6))
        df_data = final_df[x]
        count_colorid = count_color_identity(df_data)

        #ax = plt.pie(count_colorid.values(), labels=count_colorid.keys(), autopct='%.2f',colors=['Black','White','Green','Red','Blue','Grey','Orange'], pctdistance= 1.3, shadow=True, explode=(0.2,0.2,0.2,0.2,0.2,0.2,0.2))
        fig_px = px.pie(values = count_colorid.values(), names = count_colorid.keys(), color = count_colorid.keys(), color_discrete_map= color_cid)

        if(finish - start > 10):
            #ax = plt.title (f'Percentage color identity from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
            fig_px.update_layout(title = f'Percentage color identity from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            #ax = plt.title (f'Percentage color identity from {str(df_data.released_at.min())[0:4]}')
            fig_px.update_layout(title = f'Percentage color identity from {str(df_data.released_at.min())[0:4]}')
        
        #st.pyplot(fig)
        st.write(fig_px)

    total = st.checkbox('Total')

    if total:
        
        #fig,ax = plt.subplots(figsize = (15,6))
        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask]
        count_colorid = count_color_identity(df_data)
        
        #fig,ax = plt.subplots(figsize = (6,6))
        #ax = plt.pie(count_colorid.values(), labels=count_colorid.keys(), autopct='%.2f',colors=['Black','White','Green','Red','Blue','Grey','Orange'], pctdistance= 1.3, shadow=True, explode=(0.2,0.2,0.2,0.2,0.2,0.2,0.2))
        fig_px = px.pie(values = count_colorid.values(), names = count_colorid.keys(), color = count_colorid.keys(), color_discrete_map= color_cid)

        if(finish != start):
            #ax = plt.title (f'Percentage color identity from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
            fig_px.update_layout(title = f'Percentage color identity from {start} to {finish}')
        else:
            #ax = plt.title (f'Percentage color identity from {str(df_data.released_at.min())[0:4]}')
            fig_px.update_layout(title = f'Percentage color identity from {start}')
        
        #st.pyplot(fig)
        st.write(fig_px)

if attribut == 'legalities':

    color_le = {'legacy':'brown','duel':'red','vintage':'darkorange','commander':'gold','penny':'olive','modern':'lime','pauper':'turquoise','pioneer':'darkcyan','historic':'slategray','standard':'royalblues','future':'violet','brawl':'crimson','oldschool':'pink'}

    format = st.selectbox(label = 'Select a format', options=color_le.keys())

    if format in color_le.keys():
            
        for x in list_mask_data:

            #fig,ax = plt.subplots(figsize = (15,6))
            df_data = final_df[x]
            count_legalities = count_legal_cards(df_data)

            perc = {}
            perc[format] = count_legalities[format]
            perc[f'no {format}'] = len(df_data) - count_legalities[format] #totale carte - carte legali nel formato

            fig_px = px.pie(values = perc.values(), names = perc.keys(), color = perc.keys())

            if(finish - start > 10):
                #ax = plt.title (f'Percentage cards legality from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
                fig_px.update_layout(title = f'Percentage cards legality from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
            else:
                #ax = plt.title (f'Percentage cards legality from {str(df_data.released_at.min())[0:4]}')
                fig_px.update_layout(title = f'Percentage cards legality from {str(df_data.released_at.min())[0:4]}')
            
            st.write(fig_px)
        
        total = st.checkbox('Total')

        if total:

            mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
            df_data = final_df[mask]
            count_legalities = count_legal_cards(df_data)

            perc = {}
            perc[format] = count_legalities[format]
            perc[f'no {format}'] = len(df_data) - count_legalities[format] #totale carte - carte legali nel formato

            #fig,ax = plt.subplots(figsize = (6,6))
            
            #ax = plt.pie(count_legalities.values(), labels=count_legalities.keys(), autopct='%.2f',pctdistance= 1.3, shadow=True, explode=(0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2))
            fig_px = px.pie(values = perc.values(), names = perc.keys(), color = perc.keys())

            if(finish != start):
                #ax = plt.title (f'Percentage cards legality from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
                fig_px.update_layout(title = f'Percentage cards legality from {start} to {finish}')
            else:
                #ax = plt.title (f'Percentage cards legality from {str(df_data.released_at.min())[0:4]}')
                fig_px.update_layout(title = f'Percentage cards legality from {start}')

            #st.pyplot(fig)
            st.write(fig_px)

    #for x in list_mask_data:

        #fig,ax = plt.subplots(figsize = (15,6))
        #df_data = final_df[x]
        #count_legalities = count_legal_cards(df_data)

        #ax = plt.pie(count_legalities.values(), labels=count_legalities.keys(), autopct='%.2f',pctdistance= 1.3, shadow=True)
        
        #if i want to use px i have to use fig and st.write
        #fig_px = px.pie(values = count_legalities.values(), names= count_legalities.keys(), color = count_legalities.keys(), color_discrete_map = color_le)  

        #if(finish - start > 10):
            #ax = plt.title (f'Percentage cards legality from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        #    fig_px.update_layout(title = f'Percentage cards legality from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        #else:
            #ax = plt.title (f'Percentage cards legality from {str(df_data.released_at.min())[0:4]}')
        #    fig_px.update_layout(title = f'Percentage cards legality from {str(df_data.released_at.min())[0:4]}')

        #st.pyplot(fig)
        #st.write(fig_px)

    #total = st.checkbox('Total')

    #if total:

    #    mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
    #    df_data = final_df[mask]
    #    count_legalities = count_legal_cards(df_data)

        #fig,ax = plt.subplots(figsize = (6,6))
        
        #ax = plt.pie(count_legalities.values(), labels=count_legalities.keys(), autopct='%.2f',pctdistance= 1.3, shadow=True, explode=(0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2))
    #    fig_px = px.pie(values = count_legalities.values(), names= count_legalities.keys(), color = count_legalities.keys(), color_discrete_map = color_le) 

    #    if(finish != start):
            #ax = plt.title (f'Percentage cards legality from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
    #        fig_px.update_layout(title = f'Percentage cards legality from {start} to {finish}')
    #    else:
            #ax = plt.title (f'Percentage cards legality from {str(df_data.released_at.min())[0:4]}')
    #        fig_px.update_layout(title = f'Percentage cards legality from {start}')

        #st.pyplot(fig)
    #    st.write(fig_px)

if attribut == 'subtypes':

    lista_subtypes = create_lista_subtypes(final_df)
    lista_subtypes.sort()

    for x in list_mask_data:

        fig, ax = plt.subplots(figsize=(15,6))
        df_data = final_df[x]
        
        dizi_subtype = {}

        for x in lista_subtypes:
            dizi_subtype[x] = search_row_by_subtypes(x,df_data)
        #dizi_subtype
        #dizi_subtype = sorted(dizi_subtype.items(), key=lambda x: x[1], reverse=True)[0:10] #i primi 10 più frequnti subtype
        dizi_subtype = dict(sorted(dizi_subtype.items(), key = lambda item: item[1], reverse=True)[0:10])
        #dizi_subtype = dizi_subtype

        #ax = plt.bar(dizi_subtype.keys(), dizi_subtype.values())
        #CONTROLLARE
        ax = sb.barplot(x=list(dizi_subtype.keys()), y=dizi_subtype.values(), hue=list(dizi_subtype.keys()), hue_order=dizi_subtype) #colore per frequenza
        for x in ax.containers:
            ax.bar_label(x,)
        
        if(finish - start > 10):
            ax = plt.title(f'Top 10 subtype from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            ax = plt.title(f'Top 10 subtype from {str(df_data.released_at.min())[0:4]}')
        
        st.pyplot(fig)

    total = st.checkbox('Total')

    if total:

        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask]

        dizi_subtype = {}
        for x in lista_subtypes:
            dizi_subtype[x] = search_row_by_subtypes(x,df_data)
        #dizi_subtype
        #dizi_subtype = sorted(dizi_subtype.items(), key=lambda x: x[1], reverse=True)[0:10] #i primi 10 più frequnti subtype
        dizi_subtype = dict(sorted(dizi_subtype.items(), key = lambda item: item[1], reverse=True)[0:10])

        #diz = {}
        #x = 0
        #while x < len(dizi_subtype):
        #    diz[dizi_subtype[x][0]] = dizi_subtype[x][1]
        #    x +=1

        fig,ax = plt.subplots(figsize=(10,6))
        
        #ax = plt.bar(dizi_subtype.keys(), dizi_subtype.values())
        ax = sb.barplot(x=list(dizi_subtype.keys()), y=dizi_subtype.values(), hue=list(dizi_subtype.keys()), hue_order=dizi_subtype) #colore per frequenza
        for x in ax.containers:
            ax.bar_label(x,)

        if(finish != start):
            ax = plt.title(f'Top 10 subtype from {start} to {finish}')
        else:
            ax = plt.title(f'Top 10 subtype from {start}')

        st.pyplot(fig)

if attribut == 'text':
    #allora provo a ricavare le caratterisctiche proncipali 
    # flying, deathtouch, lifelink, doublestrike, vigilance ecc..
    #di solito si trovano nella prima riga
    #testo con un solo testo e poi provo a farlo su altri, forse dovrei creare una lista con le varie caratterisctiche
    #cerco solo creature
    for x in list_mask_data:

        #fig,ax= plt.subplots(figsize=(20,6))
        fig,ax= plt.subplots()
        df_data = final_df[x]

        lista_keywords_ability = {'deathtouch':0,'defender':0,'double strike':0,'enchant':0,'equip':0, 'fear':0,'first strike':0, 'flash':0, 'flying':0, 'haste':0, 'hexproof':0, 'indestructible':0, 'landwalk':0,'lifelink':0, 'menace':0, 'protection':0, 'prowess':0, 'reach':0, 'shroud':0, 'trample':0, 'vigilance':0, 'ward':0} #più comuni
        
        only_creature = search_row_by_type('Creature',df_data) #OK IN TEORIA GLIIDICI SONO DIVERSI, QUINDI NON POSSO USARE SEARCH_ROW_BY TYPE, cioè si ma non funziona dopo con iloc
        #st.write(search_row_by_type('Creature',df_data))
        #st.write(df_data.astype(str))
        #only_creature_df = df_data.iloc[only_creature] 
        only_creature_df = df_data[df_data.index.isin(only_creature)] 
        for chiave in lista_keywords_ability.keys():
            for indice,testo in only_creature_df.text.items():
                if chiave in testo.casefold():
                    lista_keywords_ability[chiave] += 1

        frequence = pd.Series(lista_keywords_ability.values(),index = lista_keywords_ability.keys())
        word_text = WordCloud(background_color="white").generate_from_frequencies((frequence))

        ax = plt.imshow(word_text)
        
        if (finish - start > 10):
            #ax = plt.title(f'Frequenci of keywords from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
            st.write(f'Frequency of keywords from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            #ax = plt.title(f'Frequenci of keywords from {str(df_data.released_at.min())[0:4]}')
            st.write(f'Frequency of keywords from {str(df_data.released_at.min())[0:4]}')
        
        ax = plt.axis("off")

        #aggiunta col
        col_df, col_word = st.columns([1,3])

        with col_df:
            st.write(frequence.sort_values(ascending=False))
        
        with col_word:
            st.pyplot(fig)
        
        #st.pyplot(fig)

    total = st.checkbox('Total')

    if total:

        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask]

        lista_keywords_ability = {'deathtouch':0,'defender':0,'double strike':0,'enchant':0,'equip':0, 'fear':0,'first strike':0, 'flash':0, 'flying':0, 'haste':0, 'hexproof':0, 'indestructible':0, 'landwalk':0,'lifelink':0, 'menace':0, 'protection':0, 'prowess':0, 'reach':0, 'shroud':0, 'trample':0, 'vigilance':0, 'ward':0} #più comuni

        only_creature = search_row_by_type('Creature',df_data)
        #only_creature_df = df_data.iloc[only_creature]
        only_creature_df = df_data[df_data.index.isin(only_creature)]
        for chiave in lista_keywords_ability.keys():
            for indice,testo in only_creature_df.text.items():
                if chiave in testo.casefold():
                    lista_keywords_ability[chiave] += 1
        
        #fig,ax = plt.subplots(figsize=(20,6))
        fig,ax = plt.subplots()
        
        #ax = plt.bar(lista_keywords_ability.keys(),lista_keywords_ability.values()) #ok bar char orribile
        #ax = addlabels(lista_keywords_ability.keys(),lista_keywords_ability.values(),limite=30000)

        #provo ad usare worldcloud
        frequence = pd.Series(lista_keywords_ability.values(),index = lista_keywords_ability.keys())
        word_text = WordCloud(background_color="white").generate_from_frequencies((frequence))

        #ax = plt.imshow(word_text, interpolation='bilinear')
        ax = plt.imshow(word_text)
        
        if (finish != start):
            #ax = plt.title(f'Frequenci of keywords from {start} to {finish}')
            st.write(f'Frequenci of keywords from {start} to {finish}')
        else:
            #ax = plt.title(f'Frequenci of keywords from {start}')
            st.write(f'Frequenci of keywords from {start}')

        ax = plt.axis("off")

        col_df, col_word = st.columns([1,3])

        with col_df:
            st.write(frequence.sort_values(ascending=False))
        with col_word:
            st.pyplot(fig)

        #st.pyplot(fig)

if attribut == 'artist':

    for x in list_mask_data:

        #fig,ax= plt.subplots() #capire che grafico usare
        df_data = final_df[x]
        
        fig_px = px.pie(values = df_data.artist.value_counts(), names=df_data.artist.value_counts().index, hole=.3)
        fig_px.update_traces(textposition='inside')
        #fig_px.update_layout(uniformtext_minsize=12, uniformtext_mode='hide') 

        if (finish - start > 10):
            st.write(f'Number of illustration for artist from {str(df_data.released_at.min())[0:4]} to {str(df_data.released_at.max())[0:4]}')
        else:
            st.write(f'Number of illustration for artist from {str(df_data.released_at.min())[0:4]}')
        
        col_df, col_don = st.columns([1,3])
        
        with col_df:
            st.write(df_data.artist.value_counts())
        
        with col_don:
            st.write(fig_px)
    
    total = st.checkbox('Total')

    if total: #start and finish totale

        #fig,ax = plt.subplots() #capire se inserire grafico
        mask = final_df['released_at'].between(f'{start}-01-01',f'{finish}-12-31')
        df_data = final_df[mask]

        fig_px = px.pie(values = df_data.artist.value_counts(), names = df_data.artist.value_counts().index, hole=.3)
        fig_px.update_traces(textposition='inside')

        if (finish != start):
            st.write(f'Number of illustration for artist from {start} to {finish}')
        else:
            st.write(f'Number of illustration for artist from {start}')

        col_df, col_don = st.columns([1,3])
        
        with col_df:
            st.write(df_data.artist.value_counts())
        
        with col_don:
            #st.write('prova, INSERIRE IMMAGINE')
            st.write(fig_px)
    

st.header('Model')

model = st.checkbox('Show model')

if model:

    #st.write('spiegazione modello, aggiungere cosa può influenzare il prezzo')
    st.write("""I have decided to implement a prediction model for card price in the project.
            The main factors influencing their cost are: rarity, legality, reprints, the number
            of copies the player needs, the condition of the card and 
            how much the card can impact the game.
            Unfortunately, some elements that influence the price were not available in 
            the dataset, so i attempt to include other variables sucha as strenght,
            costitution, mana cost and release set.""")
    #codice

    #dataframe con prezzi solo paper

    lista_ind_paper = []
    for ind in final_df.index:
        if bool(final_df.prices.iloc[ind]['paper']) == True: #prendo solo quelli che paper, in teoria
            lista_ind_paper.append(ind)
    df_prices_paper = final_df.iloc[lista_ind_paper]
    #ma se creassi una colonna apposta, mi sembra più semplice
    #creo una serie
    serie_paper = pd.Series()
    lista_prezzi_paper = []
    df_prices_paper.reset_index(inplace=True)

    for ind in df_prices_paper.index:
        prezzo = df_prices_paper.prices.iloc[ind]['paper']
        valore_prezzo = prezzo.get('2019-11-09')
        lista_prezzi_paper.append(valore_prezzo)

    df_prices_paper['price_paper'] = lista_prezzi_paper
    df_prices_paper_unique = df_prices_paper.drop_duplicates('name')
    prova_predict = df_prices_paper_unique.copy()

    #corr_prova_predict = st.checkbox('Show prova')

    #if corr_prova_predict:
    #    fig,ax = plt.subplots()
    #    ax = sb.heatmap(prova_predict.corr(numeric_only=True),annot=True, fmt=".1f", linewidth=.5)
    #    st.pyplot(fig)

    #from list/dict to string
    list_colonne_to_string = ['printings','legalities']
    
    for x in list_colonne_to_string:
        stringa = prova_predict[x].astype(str)
        col=x+'_string'
        prova_predict[col] = stringa
    
    #df per prediction
    pred = prova_predict[['rarity','price_paper','cmc','power','toughness','reprint','printings_string','set_name','legalities_string','reserved']]
    #creo a categorical variable for rarity
    categorical_feature = ['rarity','power','toughness','reserved','reprint','printings_string','legalities_string','set_name'] #ok accetta solo stringhe o numeri, devo trasformare le liste e disct in stringhe
    le = LabelEncoder()

    #convert the variable to some sort of numerical
    for i in range(8):
        new = le.fit_transform(pred[categorical_feature[i]])
        pred[categorical_feature[i]] = new
    
    pred.dropna(inplace=True)

    #training the model
    column_test = ['rarity','cmc','power','toughness','reprint','printings_string','set_name','legalities_string','reserved']
    X = pred[column_test]
    y = pred.price_paper

    #splitting data into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8,test_size=0.2, random_state=0) #capire test size e random state

    #train the model
    #regr = RandomForestRegressor(n_estimators=100, max_depth=10,  oob_score=True) 
    regr = RandomForestRegressor(n_estimators=100, min_samples_split = 2 , min_samples_leaf= 1 , oob_score=True)
    #regr = RandomForestRegressor(n_estimators=1800, min_samples_split = 10 , min_samples_leaf= 2, max_features='sqrt', max_depth= 30 , oob_score=True) #colab hyperparameter tuning random forest; {'n_estimators': 1800,'min_samples_split': 10,'min_samples_leaf': 2,'max_features': 'sqrt','max_depth': 30,'bootstrap': True}
    regr.fit(X_train, y_train.values.ravel())

    #make prediction
    warnings.filterwarnings('ignore')
    predictions = regr.predict(X_test)
    result = X_test
    result['paper_price'] = y_test
    result['prediction'] = predictions.tolist()

    #errori/risultato test
    #model evaluation
    mse = mean_squared_error(y_test.values.ravel(), predictions)
    r2 = r2_score(y_test.values.ravel(), predictions)
    mae = mean_absolute_error(y_test.values.ravel(), predictions)
    
    st.write(result)
    st.write("Mean square error (MSE):", round(mse, 2))
    st.write("R2 Score: ", round(r2, 2))
    st.write("Mean Absolute Error (MAE): ", round(mae, 2))
    oob_score = regr.oob_score_
    st.write("Out-of-Bag Score: ", round(oob_score, 2))
    
    #grafico
    
    fig,ax = plt.subplots()
    
    sort_result = result.sort_index()[450:500]
    
    price = ax.scatter(sort_result.index,sort_result.paper_price, color='blue', label = 'price')
    pred = plt.plot(sort_result.index, sort_result.prediction, color = 'red', label = 'prediction')
    #print(price)
    #print(pred)
    ax.legend(handles=[price,pred[0]])
    ax.set_xlabel('Card number')
    ax.set_ylabel('Price')
    ax.set_title('Card prices and predictions')

    st.pyplot(fig)

    st.markdown("""As could hypothesized form the absence of some important data
                such as the number of cards the player needs or the condition of the cards
                and how much the card can impact the game, the model does not perform well,
                as also indicate by the R2 score. In general, some price are predicted well, while 
                others are significantly above the normal price. On average, the mean absolute error for 
                the predicted prices is approximately $1.90""")





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

