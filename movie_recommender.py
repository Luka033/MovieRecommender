import difflib

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity




class MovieRecommender:
    def __init__(self):
        # Step 1: Read CSV File
        self.df = pd.read_csv('movie_dataset.csv')

        # Step 2: Select Features
        self.features = ['keywords', 'cast', 'genres', 'director']

        # Step 3: Create a column in DF which combines all selected features
        for feature in self.features:
            self.df[feature] = self.df[feature].fillna('')

        self.df['combined_features'] = self.df.apply(self.combine_features, axis=1)


    def combine_features(self, row):
        try:
            return row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director']
        except:
            print("Error: ", row)

    def get_movie_info(self, requested_movie_info):
        all_movie_info = ""
        for index, movie in enumerate(self.df['original_title']):
            if movie == requested_movie_info:
                all_movie_info = "Movie Title: " + str(movie) + \
                                "\n\nDirector: " + str(self.df['director'][index]) + \
                                "\n\nCast: " + str(self.df['cast'][index]) + \
                                "\n\nRating: " + str(self.df['vote_average'][index]) + \
                                "\n\nDescription: " + str(self.df['overview'][index])

        return all_movie_info


    def recommend_movie(self, movie_user_likes):
        # Find the movie most similar to users input
        new_movie_user_likes = difflib.get_close_matches(movie_user_likes, self.df['original_title'], n=1)[0]

        # Step 4: Create count matrix from this new combined column
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(self.df['combined_features'])

        # Step 5: Compute the Cosine Similarity based on the count_matrix
        cosine_sim = cosine_similarity(count_matrix)

        # Step 6: Get index of this movie from its title
        movie_index = self.get_index_from_title(new_movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))

        # Step 7: Get a list of similar movies in descending order of similarity score
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        # Step 8: Print titles of first 30 movies
        best_movies = []
        i = 0
        for movie in sorted_similar_movies:
            best_movies.append(self.get_title_from_index(movie[0]))
            i = i + 1
            if i > 30:
                break

        return best_movies

    # helper functions. Use them when needed #######
    def get_title_from_index(self, index):
        return self.df[self.df.index == index]["title"].values[0]

    def get_index_from_title(self, title):
        return self.df[self.df.title == title]["index"].values[0]



