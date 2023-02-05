"""import"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import requests
from bs4 import BeautifulSoup
import regex
from newsapi import NewsApiClient
from pymongo import MongoClient
from datetime import datetime,timezone
from datetime import timedelta
import dateutil.parser as parser

import tweepy


"""partie scraping"""

def scraping():
    #print("debut fonction scraping")
    # Définition du user-agent. J'ai utilisé Mozilla Firefox pour ce TP.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    # chargement de la page à l'adresse du site de https://www.heidi.news/articles
    page = requests.get('https://www.heidi.news/articles', headers=headers).text
    # parsing de la page web
    soup = BeautifulSoup(page, 'html.parser')

    # Je choisi l'article en entier
    articles = soup.find_all("article", class_="post post-default")

    # J'extraie la date seulement
    liste_date = []
    for el in soup.find_all('time', attrs={'class': 'post__publication-date'}):
        liste_date.append(el.get_text())
    #print(liste_date)

    # Je prend que la partie publication de la date
    date_publication_entier = []
    for i in liste_date:
        liste_split = i.split('.')
        for j in liste_split:
            if('Publié' in j):
                date_publication_entier.append(j)
    #print(date_publication_entier)

    date_ajd_entier = datetime.today()

    date_hier_entier = (date_ajd_entier - timedelta(days = 1))
    date_hier_entier_sans_heures = date_hier_entier.date()
    date_hier_str = date_hier_entier_sans_heures.strftime("%d/%m/%Y")
    #print(date_hier_str)

    date_regex = regex.compile(r'(\d{2}) (\w+) (\d{4})')

    liste_mois = {'janvier':1, 'février':2, 'mars':3, 'avril':4, 'mai':5, 'juin':6,
    'juillet':7, 'août':8, 'septembre':9, 'octobre':10, 'novembre':11, 'décembre':12}

    liste_articles = []
    for article in articles:
        liste_articles.append(article)
    #print(liste_articles)

    # on filtre pour garder que la date de publication, la date formattee sans les heures et le nombre d'articles par jour
    # on stocke ces infos dans des listes
    cpt_date_article = 1
    liste_nb_article = []
    liste_date_entier = []
    for date in date_publication_entier:
        identique = date_regex.search(date)
        jour, mois, annee = int(identique.group(1)), liste_mois[identique.group(2)], int(identique.group(3))
        if date_hier_entier.day == jour and date_hier_entier.month == mois and date_hier_entier.year == annee:
            liste_nb_article.append(cpt_date_article)
            #print(date)
            liste_date_entier.append(date)
            # affiche le contenu de l'article
            cpt_date_article += 1

    # creer un df avec les dates et le nb d'article
    data = {'source':'scraping', 'date de publication':liste_date_entier, 'date formatée':date_hier_str, 'nombre articles':liste_nb_article.pop()}
    df_scraping = pd.DataFrame(data)
    #print(df_scraping)
    return df_scraping


"""partie newsapi"""
def newsapi():
    #print("debut fonction newsapi")
    liste_date_formatee = []
    liste_date_base = []
    liste_nb_articles = []
    cpt = 1

    newsapi = NewsApiClient(api_key='4e042a4dab28440caa8d6731a17fdc47')
    data = newsapi.get_top_headlines(q='bitcoin',category='business',language='en',country='us')

    for i in data['articles']:
        date_base = i["publishedAt"]
        date_base_datetime = parser.parse(date_base)
        date_base_datetime_aware = date_base_datetime.replace(tzinfo=timezone.utc)
        date_non_iso = date_base.split("T")
        date_non_iso_var = parser.parse(date_non_iso[0])
        date_formatee = date_non_iso_var.strftime("%d/%m/%Y")


        # dates des dernieres 24h en iso 8601 offset-aware et formatee
        date_actuelle_iso = datetime.now().isoformat()
        date_actuelle_object = datetime.fromisoformat(date_actuelle_iso)
        date_24h = date_actuelle_object - timedelta(hours=24)
        date_24h_iso = date_24h.isoformat()
        date_24h_datetime = datetime.fromisoformat(date_24h_iso)
        # converti offset-naive en offset-aware
        date_24h_datetime_aware = date_24h_datetime.replace(tzinfo=timezone.utc)

        # prendre les dates des dernieres 24h et les stocker dans des listes
        # il faut que les dates du futur df soient comprise dans les dernieres 24h
        if(date_base_datetime_aware > date_24h_datetime_aware):
            liste_date_formatee.append(date_formatee)
            liste_date_base.append(date_base)
            liste_nb_articles.append(cpt)
            cpt += 1

    if len(liste_nb_articles) > 0:
        df_newsapi = pd.DataFrame({'source':'newsapi','date_formate':liste_date_formatee,'date_base':liste_date_base,'nombre articles':liste_nb_articles.pop()})
        return df_newsapi
    #print(df_newsapi)
    else:
        print("liste_nb_articles is empty")
        # df_newsapi = pd.DataFrame({'source':'news_api', 'date de publication':[], 'date formatée':[], 'nombre articles':[]})
    # return df_newsapi
    


"""partie twitter"""

def twitter():
    #Put your Bearer Token in the parenthesis below
    client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAA%2FqVQEAAAAAMTIAETuDA2dxBvBjYXWLlnemmK4%3D6dlngVslD4PzhoZR69pUvf9SUonEpobN0A5EnJoc3rY0SJwCHc')
    
    query = '#health -is:retweet lang:fr'
    tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)

    dates = []
    date_formats = []
    nombre_articles_list = 0

    date_ajd_entier = datetime.today()
    date_hier_entier = (date_ajd_entier - timedelta(days = 1))
    date_hier_entier_sans_heures = date_hier_entier.date()
    date_hier_str = date_hier_entier_sans_heures.strftime("%d/%m/%Y")

    for tweet in tweets.data:
        tweet = tweet.text
        pattern = "\d{4}-\d{2}-\d{2} \d{2}:\d{2}"
        m = regex.findall(pattern,tweet)
        
        
        if m:
            date = m[0]
            mod_date = f"{date[8:10]}/{date[5:7]}/{date[0:4]}"
            if mod_date==date_hier_str:
                
                date_formats.append(mod_date)

                date = datetime.strptime(date, '%Y-%m-%d %H:%M')
                date_format = date.isoformat()
                dates.append(date_format)
                
                nombre_articles_list += 1



    df_twitter = pd.DataFrame({'source':'twitter', 'date de publication':dates, 'date formatée':date_formats, 'nombre articles':nombre_articles_list})
    #print(df_twitter)
    return df_twitter


"""partie mongodb"""

def mongodb():
    # bd
    #print("debut fonction mongodb")
    client = MongoClient('localhost', 27017)
    print(f"client: {client}")
    # pour acceder a la bd
    db = client.mini_projet_db

    # collection
    collection = db.collection_mini_projet
    print(f"collection: {collection}")

    # supprimer les elements de la collection, pour ne pas avoir de doublons par la suite
    # result = collection.delete_many({})

    # pour connaitre le nombre d'elements supprimes
    #print(result.deleted_count, "documents supprimés.")

    # conversion du df en dictionnaire et insertion du df dans la collection
    records_scraping = df_scraping.to_dict('records_scraping')
    records_newsapi = df_newsapi.to_dict('records_newsapi')
    records_twitter = df_twitter.to_dict('records_newsapi')
    collection.insert_many(records_scraping)
    collection.insert_many(records_newsapi)
    collection.insert_many(records_twitter)

    # on compte le nombre d'element qu'il y a dans la collection actuellement
    count = collection.count_documents({})
    print(count, "documents a inserer.")

    # on affiche les elements de la collection
    # for record in collection.find():
    #     print(record)
    
    # convertit la collection en df
    data = pd.DataFrame(list(db.collection_mini_projet.find())) # ? collection.find()
    return data


"""partie visualisation"""

def visualisation_scraping():
    df_scraping_sans_date_entiere = df_collection.drop(['date de publication', '_id'], axis=1)
    df_scraping_select_source = df_scraping_sans_date_entiere.loc[df_scraping_sans_date_entiere['source'] == 'scraping'] 
    df_scraping_sans_doublons = df_scraping_select_source.drop_duplicates()
    df_scraping_sans_doublons.plot(x="date formatée", y="nombre articles", kind="bar")
    plt.title("Graphe scraping")
    plt.xlabel('date')
    plt.xticks(rotation=40)
    plt.ylabel('nombre d''articles')
    # plt.savefig('/Flask_mongo/Mini-Project/plot_scraping.png')
    #print("image scraping generee")
    plt.show()

def visualisation_newsapi():
    df_newsapi_sans_date_entiere = df_collection.drop(['date de publication', '_id'], axis=1)
    df_newsapi_select_source = df_newsapi_sans_date_entiere.loc[df_newsapi_sans_date_entiere['source'] == 'news_api'] 
    df_newsapi_sans_doublons = df_newsapi_select_source.drop_duplicates()
    df_newsapi_sans_doublons.plot(x="date formatée", y="nombre articles", kind="bar")
    plt.title("Graphe news API")
    plt.xlabel('date')
    plt.xticks(rotation=40)
    plt.ylabel('nombre d''articles')
    # plt.savefig('/Flask_mongo/Mini-Project/plot_newsapi.png')
    #print("image newsapi generee")
    plt.show()

def visualisation_twitter():
    df_newsapi_sans_date_entiere = df_collection.drop(['date de publication', '_id'], axis=1)
    df_newsapi_select_source = df_newsapi_sans_date_entiere.loc[df_newsapi_sans_date_entiere['source'] == 'twitter'] 
    df_newsapi_sans_doublons = df_newsapi_select_source.drop_duplicates()
    df_newsapi_sans_doublons.plot(x="date formatée", y="nombre articles", kind="bar")
    plt.title("Graphe Twitter")
    plt.xlabel('date')
    plt.xticks(rotation=40)
    plt.ylabel('nombre d''articles')
    #plt.savefig('/mnt/d/Bachelor_ISC2/Semestre1/2271.2_Infrastructure/Mini-projet/web/img/plot_newsapi.png')
    #print("image twitter generee")
    plt.show()

def visualisation_par_source():
    # contiendra toute les visualisations pour les afficher en meme temps
    visualisation_scraping()
    visualisation_newsapi()
    visualisation_twitter()

def visualisation_generale():
    # contient toute les visualisation de la veille en un graphe pour savoir quelle source à le plus de publication
    date_ajd_entier = datetime.today()
    date_hier_entier = (date_ajd_entier - timedelta(days = 1))
    date_hier_entier_sans_heures = date_hier_entier.date()
    date_hier_str = date_hier_entier_sans_heures.strftime("%d/%m/%Y")

    N = 3 # 3 graphes
    ind = np.arange(N) # separer les 3 graphes equitablements
    width = 0.25

    xvals = df_scraping.iloc[0]['nombre articles']
    bar1 = plt.bar(ind, xvals, width, color = 'tab:brown')
    yvals = df_newsapi.iloc[0]['nombre articles']
    bar2 = plt.bar(ind+width, yvals, width, color='tab:pink')
    zvals = df_twitter.iloc[0]['nombre articles']
    bar3 = plt.bar(ind+width*2, zvals, width, color = 'tab:olive')
    plt.xticks([]) # enlever chiffres axe x
    plt.xlabel(f"date: {date_hier_str}")
    plt.ylabel('nombre articles')
    plt.title(f"Graphe 3 sources, du {date_hier_str} par le nombre d'articles")
    plt.show()


"""partie appel de fonctions"""

df_scraping = scraping() # utile pour la bd
df_newsapi = newsapi()
df_twitter = twitter()
df_collection = mongodb()
print(df_collection)
visualisation_generale()
visualisation_par_source()

sys.excepthook = lambda *args: print("Bye")
