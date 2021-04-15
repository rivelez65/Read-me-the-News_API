import pyttsx3
import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# LOAD API KEY FROM ENV VARIABLES
load_dotenv()
APINEWS_KEY = os.environ.get('API_KEY')

# DATES FOR QUERY
TODAY = datetime.datetime.today().date()
MONTH_AGO = TODAY - datetime.timedelta(30)

# API URL
URL_APINEWS = 'http://newsapi.org/v2/everything?'


# MAKE REQUEST AND GET THE FIRST URL
def get_article(search):

    # SETUP REQUEST PARAMETERS TO FETCH ARTICLES FROM API NEWS
    api_params = {
        'q': f'"{search}"',
        'qInTitle': search,
        'sortBy': 'publishedAt',
        'from': MONTH_AGO,
        'to': TODAY,
        'apiKey': APINEWS_KEY,
        'language': 'en'
    }
    relevant_news = requests.get(url=URL_APINEWS, params=api_params)
    relevant_news.raise_for_status()
    return relevant_news.json()['articles'][0]['url']


while True:
    # USER INPUT QUERY TO FIND NEWS ARTICLES
    SUBJECT = input('\nSEARCH FOR NEWS: ')
    try:
        news = get_article(SUBJECT)
    except IndexError:
        print(f'Nothing found for {SUBJECT}, Try a new search query')
        SUBJECT = input('\nSEARCH FOR NEWS: ')
        news = get_article(SUBJECT)

    # NEW REQUEST TO FIRST ARTICLE'S URL
    response = requests.get(news)
    new_webpage = response.text

    # PARSE HTML USING BEAUTIFUL SOUP
    soup = BeautifulSoup(new_webpage, "html.parser")
    print(news)

    # GET NEWS HEADLINE
    title = soup.title.string

    # GET NEWS ARTICLE'S TEXT
    article = soup.find_all(name='p')
    text = ''.join(str(p.get_text()) for p in article)
    print(text)

    # CONCAT STRING CONTAINING TITLE AND BODY OF ARTICLE
    read = title + text

    # INITIATE TEXT TO SPEECH
    engine = pyttsx3.init()

    # TO CHANGE VOICE LANGUAGE OR GENDER************************************************
    # def change_voice(engine, language, gender='VoiceGenderFemale'):
    #     for voice in engine.getProperty('voices'):
    #         if language in voice.languages and gender == voice.gender:
    #             engine.setProperty('voice', voice.id)
    #             return True
    #
    #     raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))
    #
    #
    # change_voice(engine, "en_US", "VoiceGenderFemale")

    # SET RATE
    engine.setProperty("rate", 200)

    # READ NEWS ARTICLE
    engine.say(read)
    engine.runAndWait()
