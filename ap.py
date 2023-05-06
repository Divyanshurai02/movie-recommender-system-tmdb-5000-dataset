import streamlit as st
import pickle
import requests
import pandas as pd

movies_list = pickle.load(open('movies.pkl', 'rb'))

movies_listt = movies_list['title'].values
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(movies_list['tags']).toarray()
cv.get_feature_names()
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)



def f_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=200705b8080c4bc677f5d82c456ec237".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:5]
    recommended_movies = []
    poster = []
    for i in movies:
        movies_id = movies_list.iloc[i[0]].movie_id
        # fetch_poster from Api
        poster.append(f_poster(movies_id))
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies, poster


st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'CHOOSE AND GET 4 SIMILAR  MOVIES',
    movies_listt)


if st.button('Recommend'):
    names, pictures = recommend(selected_movie_name)
    col1, col2 = st.columns(2,gap="small")

    with col1:
        st.subheader(names[0])
        st.image(pictures[0])

    with col2:
        st.subheader(names[1])
        st.image(pictures[1])

    col3, col4= st.columns(2, gap="small")

    with col3:
        st.subheader(names[2])
        st.image(pictures[2])

    with col4:
        st.subheader(names[3])
        st.image(pictures[3])
    
