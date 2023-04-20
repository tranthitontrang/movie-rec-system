# movie-rec-system
Movie recommendation system using training data from Kaggle

Dataset: The MovieLens dataset on Kaggle
(https://www.kaggle.com/grouplens/movielens-20m-dataset)

Technical plan:
1. Data preparation: Preparing and cleaning dataset for analysis by remove of
duplicates, handling missing values, and converting variables
2. Primary data visualization: Calculating summary statistics and conduct data
visualization to identify patterns trends and exploratory insights
3. Collaborative Filtering: Using collaborative filtering techniques (user-based
or item-based) to predict user preferences.
4. Evaluate performance: Using metrics (Mean Absolute Error (MAE), Root
Mean Squared Error (RMSE), ect..) to evaluate the performance of the
recommendation system.
5. Deployment: Deploy the system in UI that lets users input their preferences
and receive movie recommendations accordingly.

Tools:
- Python: for data preparation and analysis
- Pandas library: analyzing, cleaning, manipulating dataset
- Scikit-learn: collaborative filtering techniques
- Flask: for deploying the project as a web-app

Preliminary plan for the code (can be edited/elaborated further)
- Interface set up for users (perhaps web interface/html). Users can pick/input x amount of movies they like or rate x amount of movies.
- Machine learning model trained on the dataset consisting of movie data. Perhaps a user-based collaborative filtering or clustering model (k-nearest neighbor model?)
- ML model suggests movie(s) to watch based on preferences.
- A plan for principle of suggestions: User A using the recommendation site likes movies x and y. Find users with similar movie preferences. User B from the dataset likes movies x, y, and z. Suggest movie z to User A. Liking could be based on user ratings.
- Alternative plan: Cluster movies based on user ratings and genres. Determine what movies and genres User A likes based on ratings inputted. Suggest movies which have been clustered close to the liked movies.
