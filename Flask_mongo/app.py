from flask import Flask, render_template, abort,send_from_directory
from pymongo import MongoClient
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from io import BytesIO
import base64
import matplotlib
matplotlib.use('agg')
import os
import sys
import nltk
nltk.download('punkt')

app = Flask(__name__)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('C:/Users/stefa/Desktop/Fiverr/suis/Flask_mongo/templates/Mini-Project/', filename)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/500')
def error500():
    abort(500)

@app.route('/templates/<int:idx>')
def message(idx):
    messages = ['Message Zero', 'Message One', 'Message Two']
    try:
        return render_template('message.html', message=messages[idx])
    except IndexError:
        abort(404)

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route("/get_plot")
def index():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['trends-newsapi']
    collection = db['articles']

    # Retrieve data from MongoDB
    data = list(collection.find())
    text = [d['title'] for d in data]

    # Tokenize the text
    tokens = nltk.word_tokenize(" ".join(text))

    # Get the frequency distribution of the tokens
    fdist = FreqDist(tokens)

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Plot the frequency distribution
    fdist.plot(30, cumulative=False)

    # Save the figure to a buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert the figure to base64
    image_base64 = base64.b64encode(buf.getvalue()).decode()
     # Close the figure
    plt.close(fig)
    # i want to return ths html page with the image
    return render_template('index.html', image_base64=image_base64)
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
