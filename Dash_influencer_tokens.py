

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

INFLUENCER_NAME = 'Bullrun_Gravano'
TWEETS_SINCE = '2021-01-01'
LIMIT_TWEETS = 1000


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










