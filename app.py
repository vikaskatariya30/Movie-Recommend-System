import streamlit as st
import pandas as pd
import pickle
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create a session with retry logic once, reuse it across calls
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d6d9c7cc91f881ac71644236e1e95cf1&language=en-US"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movie_list=sorted(list(enumerate(distance)), reverse=True, key=lambda x:x[1])[1:6]

    recommendation_movie=[]
    recommend_movie_poster=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        
        
        recommendation_movie.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommend_movie_poster.append(fetch_poster(movie_id))

    return recommendation_movie, recommend_movie_poster

movies_dict=pickle.load(open('movies_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommendation System")

select_movie=st.selectbox(
'Select a movie from the list.....',
movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(select_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])