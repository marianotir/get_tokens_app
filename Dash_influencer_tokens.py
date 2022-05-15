

# ----------------------------
# Load libraries
# ----------------------------

import snscrape.modules.twitter as sntwitter
import pandas as pd
import glob
import os
# import coinmarketcapapi
import streamlit as st

pd.set_option('display.max_columns',6)


# ----------------------------
# Define Global Variables
# ----------------------------

# INFLUENCER_NAME = 'Bullrun_Gravano'
TWEETS_SINCE = '2021-01-01'
LIMIT_TWEETS = 100


# ----------------------------
# Define Functions
# ----------------------------


def get_tokens(INFLUENCER_NAME,TWEETS_SINCE,LIMIT_TWEETS):
    # ----------------------------
    # Get tweets
    # ----------------------------

    # Creating list to append tweet data to
    tweets_list = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('since:'+TWEETS_SINCE+' from:'+INFLUENCER_NAME).get_items()):
        if i>LIMIT_TWEETS-1:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

    # Creating a dataframe from the tweets list above
    df_influencer_tweets = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

    print('Numero de tweets ' + INFLUENCER_NAME + ': ' + str(len(df_influencer_tweets)))


    # ----------------------------
    # Get tokens
    # ----------------------------

    def has_numbers(inputString):
        return any(char.isdigit() for char in inputString)

    df_influencer_tweets = df_influencer_tweets.reset_index()
    show_tweets = False
    for index, row in df_influencer_tweets.iterrows():
        text = row['Text']
        token_found = ''
        if show_tweets:
            print('Analyzing following text:')
            print(' ################ ')
            print(text)
        for word in text.split():
            if '$' in word and has_numbers(word)==False:
                word = word.replace(",", "")
                word = word.replace(".", "")
                word = word.replace("?", "")
                word = word.replace("!", "")
                word = word.replace("$", "")
                word = word.replace(";", "")
                word = word.replace("-", "")
                word = word.replace("…", "")
                word = word.replace("😂", "")
                word = word.replace("👇🏾", "")
                word = word.replace("jokes", "")
                word = word.replace("btc", "")
                word = word.replace(")", "")
                word = word.replace("#", "")
                word = word.replace("/", "")
                word = word.upper()
                if(len(word)>2):
                     token_found = word

        df_influencer_tweets.loc[index,'tokens_detected'] = token_found

    df_influencer_tweets = df_influencer_tweets[df_influencer_tweets['tokens_detected']!='']

    df_influencer_tweets['Day'] = df_influencer_tweets.Datetime.dt.day
    df_influencer_tweets['Month'] = df_influencer_tweets.Datetime.dt.month
    df_influencer_tweets['Year'] = df_influencer_tweets.Datetime.dt.year
    df_influencer_tweets['WeekOfYear'] = df_influencer_tweets.Datetime.dt.weekofyear

    tokens_influencer = df_influencer_tweets.tokens_detected.unique().tolist()

    print('Total tokens tweet by influencer ' + INFLUENCER_NAME + ': ' + str(len(tokens_influencer)))

    print('Token load completed')

    return tokens_influencer

'''
    # ----------------------------
    # Get tokens addresses
    # ----------------------------
    # Note: From here the token address are used and then the excel files can be downloaded manually

    # api_key = 'ee1fba7d-e6ba-4d59-847f-29d45165abb0'
    cmc = coinmarketcapapi.CoinMarketCapAPI(api_key)

    data_id_map = cmc.cryptocurrency_map()

    name = []
    symbol = []
    chain = []
    address = []
    status = []
    for data in data_id_map.data:
        symbol_token = data['symbol']
        if symbol_token in tokens_influencer:
            name.append(data['name'])
            symbol.append(data['symbol'])
            try:
                chain.append(data['platform']['name'])
                address.append(data['platform']['token_address'])
                status.append('chain found')
            except:
                chain.append(data['name'])
                address.append(data['slug'])
                status.append('chain not found')

    df_token_list = pd.DataFrame({'name':name,'symbol':symbol,'chain':chain,'token_address':address,'status':status})

    df_eth = df_token_list[df_token_list['chain']=='Ethereum']
    tokens_eth = df_eth.symbol.unique()

    df_bnb = df_token_list[df_token_list['chain']=='BNB Smart Chain (BEP20)']
    tokens_bnb = df_bnb.symbol.unique()

    tokens = df_token_list.symbol.unique()

    print('TOTAL tokens Ethereum:')
    print(tokens_eth)

    print('TOTAL tokens Binance:')
    print(tokens_bnb)
    

    '''
    # save token list
    # file_name = 'tokens_' + INFLUENCER_NAME + '.xlsx'
    # path = rf'C:\Users\marianota\Projects\TOKENS_ANALYSIS\\'
    # path = rf'C:\Users\{os.getlogin()}\Downloads\\'
    # file_path = path + file_name
    # writer = pd.ExcelWriter(file_path,engine='xlsxwriter')
    # df_token_list.to_excel(writer, sheet_name='Tokens', index=False)
    # writer.save()



# -----------------------------
# Build Streamlit dashboard
# -----------------------------

st.title('GET TOKENS FROM INFLUENCERS')

# st.write(" GET TOKENS FROM INFLUENCERS ")

INFLUENCER_NAME = st.text_input("Twitter Account Name: ", 'input here')


if st.button('Load Tokens'):

    with st.spinner('Finding tokens'):

        tokens_found = get_tokens(INFLUENCER_NAME,TWEETS_SINCE,LIMIT_TWEETS)

        st.success('Done!')

    st.write('Token found completed')

    st.write('Tokens found:')

    st.write(tokens_found)










