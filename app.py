import streamlit as st
import pickle
import pandas as pd
import requests


# Fetch the poster of the movie using The Movie DB API
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8b04d3c92c06724b4469d4230bf45cdf&language=en-US")
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching movie poster: {e}")
        return "https://via.placeholder.com/500x750?text=Poster+Not+Available"


# Recommend function to find similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load movie data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit page configuration for Amazon Prime Video Theme
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Main Header with Prime Video Aesthetic
st.markdown(
    """
    <style>
    .main-header {
        font-size:45px;
        font-weight: bold;
        text-align: center;
        color: #00A8E1;
        background-color: #0F171E;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
    }
    .sub-header {
        font-size: 20px;
        text-align: center;
        color: #D1D1D1;
        margin-bottom: 30px;
    }
    .poster-text {
        font-size:18px; 
        color:#FFFFFF; 
        background-color:#1A1A1A; 
        padding: 8px; 
        border-radius: 8px;
        text-align: center;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.4);
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #999;
        margin-top: 40px;
    }
    body {
        background-color: #0F171E;
        font-family: 'Helvetica', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="main-header">🎥 Movie Recommender System 🎥</div>', unsafe_allow_html=True)

# Add description with Prime Video style
st.markdown(
    '<div class="sub-header">Find movies you’ll love, just like browsing Prime Video! Select your favorite movie, and we’ll show you similar recommendations.</div>',
    unsafe_allow_html=True)

# Select a movie dropdown
selected_movie_name = st.selectbox(
    'Choose your favorite movie from the list:',
    movies['title'].values
)

# Button for recommendations with Prime Video style
if st.button('Recommend Movies 🎬'):
    names, posters = recommend(selected_movie_name)

    st.markdown("<h3 style='text-align: center; color: #00A8E1;'>Recommended Movies:</h3>", unsafe_allow_html=True)

    # Display recommended movies with larger posters in Prime Video theme
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.image(posters[i], width=220)  # Larger poster for Prime-style look
            st.markdown(f"<div class='poster-text'>{names[i]}</div>", unsafe_allow_html=True)

# Footer Section in Prime Video style
st.markdown(
    """
    <hr style='border: 1px solid #333;'>
    <div class="footer">Built with ❤️ by Piyush Kumar using Python and Streamlit</div>
    """, unsafe_allow_html=True
)

# Styling the Streamlit interface with Prime Video color scheme
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #00A8E1;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(0, 168, 225, 0.4);
    }
    .stButton>button:hover {
        background-color: #007EBA;
        box-shadow: 0px 4px 8px rgba(0, 126, 186, 0.4);
    }
    .stSelectbox label {
        font-size: 16px;
        color: #FFFFFF;
    }
    .stSelectbox>div>div {
        background-color: #1A1A1A;
        color: white;
        border: 1px solid #00A8E1;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True
)

