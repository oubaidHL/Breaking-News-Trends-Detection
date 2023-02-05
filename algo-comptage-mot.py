import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from pymongo import MongoClient


#nltk.download('stopwords')
# Connexion à la base de données MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["trends-newsapi"]

# Récupération des articles de presse de la base de données
articles = list(db.articles.find({}))

# Conversion des articles en un DataFrame pandas
articles_df = pd.DataFrame(articles)


# Nettoyage des articles (suppression des stopwords et des caractères spéciaux)
stop_words = set(stopwords.words("french"))

articles_df['description'] = articles_df['description'].apply(lambda x: ' '.join([word for word in word_tokenize(str(x)) if word.isalnum() and word not in stop_words]))

# Calcul des mots les plus fréquents
words = ' '.join(articles_df['description'])
fdist = FreqDist(words.split())
top_words = fdist.most_common(20)
print(top_words)

#Fermeture de la connexion avec la base de données
client.close()