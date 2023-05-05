from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
from fuzzywuzzy import fuzz
import re

import os
port = int(os.environ.get('PORT', 5000))


# Load movie data and define the movie recommendation functions
movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/rating.csv")
tags = pd.read_csv("data/tag.csv")

def find_similar_movies(movie_id):
    # Get the ratings for the movie
    movie_ratings = ratings[ratings["movieId"] == movie_id]
    
    # Get the users who rated the movie
    users = list(movie_ratings["userId"])
    
    # Get the movies that these users have rated
    user_ratings = ratings[ratings["userId"].isin(users)]
    
    # Calculate the average rating for each movie
    avg_ratings = user_ratings.groupby("movieId")["rating"].mean().reset_index()
    
    # Merge the movie data with the average ratings
    movie_ratings = pd.merge(movies, avg_ratings, on="movieId")
    
    # Find the movies that are most similar to the target movie
    target_movie = movie_ratings[movie_ratings["movieId"] == movie_id]
    target_genres = set(target_movie["genres"].values[0].split("|"))
    target_tags = set(tags[tags["movieId"] == movie_id]["tag"].values)
    
    similar_movies = movie_ratings[movie_ratings["movieId"] != movie_id]
    similar_movies["similarity"] = similar_movies.apply(lambda x: 
        fuzz.ratio(target_movie.iloc[0]["title"].lower(), x["title"].lower()) / 100
        + len(target_genres & set(x["genres"].split("|"))) / len(target_genres)
        + len(target_tags & set(tags[tags["movieId"] == x["movieId"]]["tag"].values)) / len(target_tags),
        axis=1
    )
    similar_movies = similar_movies.sort_values(by="similarity", ascending=False).head(10)
    
    return similar_movies


def search(title):
    # Preprocess the input
    title = title.strip().lower()
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    
    # Look up movies that match the search query using fuzzy matching
    results = []
    for _, row in movies.iterrows():
        row_title = re.sub(r'[^a-zA-Z0-9\s]', '', row['title'].lower())
        ratio = fuzz.ratio(title, row_title)
        if ratio >= 70:
            results.append(row)
            
    results_df = pd.DataFrame(results)
    
    # If no results are found, return an empty DataFrame
    if results_df.empty:
        return pd.DataFrame()
    
    # Get the movieId of the first movie in the results
    movie_id = results_df.iloc[0]["movieId"]
    
    # Find similar movies based on collaborative filtering
    similar_movies = find_similar_movies(movie_id)
    
    # Return the list of similar movies
    return similar_movies.to_html()

# Create a Flask app
app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Define a route that handles the user input and returns the movie recommendations
@app.route('/recommendations', methods=['POST'])
def recommendations():
    title = request.form['title']
    results = search(title)
    session['results'] = results
    session['title'] = title
    return redirect(url_for('home'))

# Define a route that renders a template with a form for user input
@app.route('/')
def home():
    results = session.pop('results', None)
    title = session.pop('title', None)
    return render_template('home.html', results=results, title=title)



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=port)

    