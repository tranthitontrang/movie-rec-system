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

