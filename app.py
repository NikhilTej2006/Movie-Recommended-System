import streamlit as st
import pickle
import pandas as pd
import requests

# --- Page Config ---
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Montserrat', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }

        .title {
            text-align: center;
            font-size: 3.2em;
            font-weight: bold;
            color: #fddb3a;
            margin-bottom: 0.5em;
        }

        .subtitle {
            font-size: 1.2em;
            text-align: center;
            color: #eeeeee;
            margin-bottom: 2em;
        }

        .stButton>button {
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            color: white;
            border: none;
            border-radius: 30px;
            padding: 0.6em 2em;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(to right, #ff4b2b, #ff416c);
        }

        .movie-card {
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.05);
            padding: 1em;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
            backdrop-filter: blur(8px);
            transition: 0.3s ease;
        }

        .movie-card:hover {
            transform: scale(1.05);
            background: rgba(255, 255, 255, 0.1);
        }

        .movie-title {
            margin-top: 0.5em;
            font-weight: bold;
            font-size: 1em;
            color: #ffdd57;
        }
    </style>
""", unsafe_allow_html=True)

# --- Function to fetch poster ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/300x450.png?text=No+Image"

# --- Recommendation logic ---
def recommend(movie):
    movie_ind = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_ind]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies, recommended_movies_posters = [], []
    for i in movies_list:
        mid = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(mid))
    return recommended_movies, recommended_movies_posters

# --- Load Data ---
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# --- UI Layout ---
st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find your next favorite movie 🎥🍿</div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox("🎞️ Choose a movie:", movies['title'].values)

if st.button("🎯 Recommend Movies"):
    names, posters = recommend(selected_movie_name)
    st.markdown("## 🌟 Recommended for you:")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(posters[i], use_column_width=True)
            st.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
