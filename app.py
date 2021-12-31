import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Sentiment analysis con i tweet 🐦")
st.sidebar.title("Sentiment analysis con i tweet 🐦")

st.markdown("Prima dashboard con Streamlit")
st.sidebar.markdown("Prima dashboard con Streamlit")

DATA_URL = ("./us-airline-tweets.csv")


@st.cache(persist = True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader("Mostra un tweet")
random_tweet_radiobtn = st.sidebar.radio('Scegli in base al sentiment', ('positive', 'neutral', 'negative'))
random_tweet = data.query('airline_sentiment == @random_tweet_radiobtn')[["text"]].sample(n=1).iat[0,0]
html_tw = f"""
<style>
.tweet {{
font-family:sans-serif;
color:#24a9e1;
font-size:18px;
line-height:1.2;
font-weight:bold;
}}
</style>
<p class="tweet">
{random_tweet}
</p>
"""
st.sidebar.markdown(html_tw, unsafe_allow_html=True)


st.sidebar.markdown('# GRAFICI')
st.sidebar.markdown('## 1. La distribuzione dei tweet')
select = st.sidebar.selectbox('', ['Colonne', 'Torta'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if st.sidebar.checkbox('Mostra grafico', True, key='1'):
    if select == "Colonne":
        fig = px.bar(sentiment_count, x = 'Sentiment', y = 'Tweets', color='Tweets', height = 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values = 'Tweets', names = 'Sentiment')
        st.plotly_chart(fig)

st.sidebar.markdown('## 2. Mappa: quando e dove gli utenti hanno tweetato')
hour = st.sidebar.slider('Scegli l\'ora del giorno', 0, 23)
selected_data = data[data['tweet_created'].dt.hour == hour]

if st.sidebar.checkbox("Mostra mappa", True, key='2'):
    st.markdown("%i tweets between %i:00 and %i:00" % (len(selected_data), hour, (hour+1)%24))
    st.map(selected_data)
    if st.sidebar.checkbox("Mostra tabella dati", True):
        st.write(selected_data)



st.sidebar.markdown('## 3. I tweet per compagnia aerea')
choice = st.sidebar.multiselect('Scegli la compagnia', ('American', 'Delta', 'Southwest', 'United', 'US Airways', 'Virgin America'), default=["American"], key = '0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x = 'airline', y = 'airline_sentiment', histfunc = 'count', color = 'airline_sentiment', facet_col = 'airline_sentiment', labels = {'airline_sentiment':'tweets'}, height = 400, width = 600)
    st.plotly_chart(fig_choice)


st.sidebar.header("Word cloud")
word_sentiment = st.sidebar.radio('Mostra word cloud in base al sentiment', ('positive', 'neutral', 'negative'), index = 0)

if st.sidebar.checkbox("Mostra World Cloud", True, key='3'):
    st.header('Word cloud per il sentiment %s' % (word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT' ])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height = 650, width = 800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
