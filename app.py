from flask import Flask, request, render_template
import surprise
from surprise import accuracy
from surprise import KNNBasic
from surprise import Dataset
from surprise.model_selection import train_test_split

#**Prepare datasets for training and testing**

movie_data = Dataset.load_builtin('ml-100k')
#Split the Movielens dataset into a 75%/25% train and test set:
trainset, testset = train_test_split(movie_data, test_size=.2, random_state=42)
trainset.ur[590]

#**Training A Recommender System**

movie_recommender = KNNBasic()
movie_recommender.fit(trainset)

#**Evaluating Recommender System Performance**
#Create some predictions on the test set
predictions = movie_recommender.test(testset)

# Measure of RMSE (root-mean square error)
accuracy.rmse(predictions)

#create Flask route
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

#Create another Flask route that handles the form submission and returns the recommended movies.
@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = request.form['user_id']
    movie_id = request.form['movie_id']
    rating = request.form['rating']
    
    # Add the new user to the training set
    trainset_new = trainset.build_full_trainset()
    trainset_new.add_rating(user_id, movie_id, rating)
    
    # Train the recommender system on the updated training set
    movie_recommender.fit(trainset_new)
    
    # Generate movie recommendations for the new user
    recommendations = movie_recommender.get_top_n(trainset_new, n=10)
    
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True) 
