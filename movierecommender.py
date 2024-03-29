# -*- coding: utf-8 -*-
"""MovieRecommender.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LeNpkhtTY1wSkXxsaMvcVhzjN0VsdDTm
"""

# Recommneder system

# collaborative filtering - based on other people experiences and ratings
# content-based recommender -> done based on the customer experience


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# Load movie metadata
movie_metadata = pd.read_csv("https://modcom.co.ke/datasets/movie_metadata.csv")

# Load user-item ratings
user_item_details = pd.read_csv("https://modcom.co.ke/datasets/file.csv")

# Merge movie metadata with user-item ratings
data = pd.merge(user_item_details, movie_metadata, on='movie_id')

# Create a pivot table of the user-item ratings
pivot = data.pivot_table(index='user_id', columns='title', values='rating')

# Create a TF-IDF vectorizer to extract features from the movie overview text
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movie_metadata['overview'].fillna(''))

# Compute cosine similarity between all movies
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Helper function to get movie recommendations based on content similarity
def get_content_based_recommendations(user_id, title, cosine_sim=cosine_sim,  pivot=pivot, movie_metadata=movie_metadata):
    # Get the index of the movie
    idx = movie_metadata[movie_metadata['title'] == title].index[0]

    # Get the cosine similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the cosine similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie titles from the indices
    movie_indices = [i[0] for i in sim_scores]
    movie_titles = movie_metadata['title'].iloc[movie_indices].values

    # Get the user's ratings for all movies
    user_ratings = pivot.loc[user_id]

    #Get the similar movies rated by the user
    similar_movies = pivot.corrwith(user_ratings).dropna()
    similar_movies = similar_movies.sort_values(ascending=False)

     # Get the top 10 most similar movies based on collaborative filtering
    similar_movies = similar_movies[similar_movies.index.isin(movie_metadata['title'])]
    movie_titles_collab = similar_movies.index[:10].values

    # Combine the content-based and collaborative filtering recommendations
    movie_titles_hybrid = list(set(movie_titles_content).union(set(movie_titles_collab)))

    return movie_titles_hybrid


# movie datasets

movie_details = pandas.read_csv("https://modcom.co.ke/datasets/Movie_Id_Titles.csv")
movie_details.head(50)

# merging two datasets
data = pandas.merge(user_item_details,movie_details, on='item_id')
data

# group by title , rating

data.groupby('title')['rating'].mean().sort_values(ascending=False)

data.groupby('title')['rating'].count().sort_values(ascending=False)

# store mean rating

mean_ratings = pandas.DataFrame(data.groupby('title')['rating'].mean())
mean_ratings

# column for number of ratings
mean_ratings['number_of_ratings'] = pandas.DataFrame(data.groupby('title')['rating'].count())
mean_ratings

# pivot table
# index, columns, values

pivot = data.pivot_table(index='user_id', columns='title', values='rating')
pivot

# movie selection

selected_movie = pivot['Batman (1989)']

similar = pivot.corrwith(selected_movie)
similar_df = pandas.DataFrame(similar, columns=['correlations'])
similar_df.sort_values('correlations', ascending=False)

# join similar_df with mean_ratings

similar_df = similar_df.join(mean_ratings['number_of_ratings'])
similar_df

# recommended movies
similar_df[similar_df['number_of_ratings'] > 200].sort_values('correlations', ascending=False).head(20)

# read new dataset containing movie attributes
movie_attributes = pandas.read_csv("https://modcom.co.ke/datasets/Movie_Attributes.csv")

# merge the new dataset with the existing dataset based on the 'item_id' column
data = pandas.merge(data, movie_attributes, on='item_id')

# create a new DataFrame with the 'item_id' and 'title' columns
movie_info = data[['item_id', 'title']].drop_duplicates()

# create a TF-IDF vectorizer to extract important keywords from the plot summary of each movie
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')

# apply the TF-IDF vectorizer to the plot summary of each movie to obtain a sparse matrix
plot_matrix = tfidf.fit_transform(data['plot'])

# compute the cosine similarity between each pair of movies based on their sparse matrix
from sklearn.metrics.pairwise import cosine_similarity
cosine_similarities = cosine_similarity(plot_matrix)

# for a selected movie, compute the cosine similarity between that movie and all other movies
selected_movie_id = 123 # replace with the actual item_id of the selected movie
selected_movie_index = movie_info[movie_info['item_id'] == selected_movie_id].index[0]
similarities = list(enumerate(cosine_similarities[selected_movie_index]))

# combine the similarity scores from collaborative filtering and content-based filtering using a weighted average
alpha = 0.5 # weight for collaborative filtering
beta = 0.5 # weight for content-based filtering
combined_similarities = [(alpha * similar_df['correlations'][i]) + (beta * similarity) for i, similarity in similarities]

# recommend the top N movies based on the combined similarity scores
N = 20 # number of recommendations to generate
recommended_indices = [i[0] for i in sorted(enumerate(combined_similarities), key=lambda x:x[1], reverse=True)[1:N+1]]
recommended_movies = movie_info.iloc[recommended_indices]['title']
