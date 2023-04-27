from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd

import os
port = int(os.environ.get('PORT', 5000))


#Load your movie data and define the movie recommendation functions
movies = pd.read_csv("movies.csv")

def find_similar_movies(movie_id):
    movie = movies[movies["movieId"] == movie_id]
    genre = movie.iloc[0]["genres"]
    similar_movies = movies[movies["genres"] == genre]
    similar_movies = similar_movies[similar_movies["movieId"] != movie_id]
    return similar_movies.head(10)

def search(title):
    # Look up movies that match the search query
    results = movies[movies['title'].str.contains(title, case=False)]
    
    # If no results are found, return an empty DataFrame
    if results.empty:
        return pd.DataFrame()
    
    # Get the movieId of the first movie in the results
    movie_id = results.iloc[0]["movieId"]
    
    # Find similar movies based on genre
    similar_movies = find_similar_movies(movie_id)
    
    # Return the list of similar movies
    return similar_movies.to_html()

#Create a Flask app
app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.run(host='0.0.0.0', port=port)

#Define a route that handles the user input and returns the movie recommendations
@app.route('/recommendations', methods=['POST'])
def recommendations():
    title = request.form['title']
    results = search(title)
    session['results'] = results
    session['title'] = title
    return redirect(url_for('home'))

#Define a route that renders a template with a form for user input
@app.route('/')
def home():
    results = session.pop('results', None)
    title = session.pop('title', None)
    return render_template('home.html', results=results, title=title)


#Run the app
if __name__ == '__main__':
    app.run(debug=True)

