import streamlit as st
import pickle
import pandas as pd
import requests

# Load the saved data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

new_df = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=fd32045bccca6a2919d5bc4010b1c8c8&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation function
def recommend(movie):
    # find index of the movie
    movie_index = new_df[new_df['title'] == movie].index[0]

    # get similarity scores for that movie
    distances = similarity[movie_index]

    # sort by similarity (skip the 1st one because it’s the same movie)
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = new_df.iloc[i[0]].movie_id  # get actual movie_id from dataframe
        recommended_movies.append(new_df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


# Streamlit UI
st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Which movie do you want recommendations for?',
    new_df['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # create 5 columns for posters
    cols = st.columns(5)
    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
