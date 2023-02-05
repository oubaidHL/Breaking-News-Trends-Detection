import tweepy
import requests
import pymongo
from datetime import datetime
import schedule
import time

def gettrends():
    # Authentification avec Twitter API
    consumer_key ="xxNK14q2MELn6ffUs1rN6UlcQ"
    consumer_secret ="dW4G9aUdpS9TmGG4KXeRVpcqJt8LPOv8e8t86qnhKJd9hr5FlD"
    access_token ="1587916737533591558-MpWViaDE1uYdMFlMOTWkeCif4NR5sp"
    access_token_secret ="w30bA7ilJ0Wk3XbMUTwfZcAOkRCOoVSaGX0cD0HxkS9ZP"

    #    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    #    auth.set_access_token(access_token, access_token_secret)
    #    api = tweepy.API(auth)

    # Récupération des tweets avec le mot clé "BREAKING NEWS"
    #tweets = api.search_tweets(q='BREAKING NEWS', count=100)

    # Connexion à la base de données MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["trends-newsapi"]

        # Boucle pour stocker les tweets dans la base de données
        #for tweet in tweets:
        #    db.tweets.insert_one({
        #        "username": tweet.user.screen_name,
        #        "text": tweet.text,
        #        "created_at": tweet.created_at,
        #        "location": tweet.user.location
        #    })
            
        # Récupération des articles de presse récents à l'aide de l'API de News
    news_api_key = '1169125a7aee4d07a6c4eccce9845a08'
    url = 'https://newsapi.org/v2/top-headlines?category=business&language=fr&apiKey=' + news_api_key
        #PARAMS = {'from':'2023-01-01','to':'2023-01-27'}
    response = requests.get(url)
    articles = response.json()['articles']

        # Boucle pour stocker les articles de presse dans la base de données
    for article in articles:
            db.articles.insert_one({
                "title": article['title'],
                "description": article['description'],
                "url": article['url'],
                "published_at": article['publishedAt'],
                "source": article['source']['name']
            })
        
        #Fermeture de la connexion avec la base de données
    client.close()
schedule.every().day.at("17:00").do(gettrends)
while True:
    schedule.run_pending()
    time.sleep(1)