import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    api_key = "a546b07dbf904f1ed84157fb7938027c"
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
    data = response.json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path

# Function to get movie recommendations
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        # fetch poster from API
        recommended_movies.append((movies.iloc[i[0]].title))
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity data
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Custom SessionState class
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Initialize session state
if 'state' not in st.session_state:
    st.session_state['state'] = SessionState(recent_searches=[])

# Streamlit app
menu_options = ['Movie Recommender', 'All Movies']
selected_menu = st.sidebar.selectbox('Menu', menu_options)

if selected_menu == 'Movie Recommender':
    st.title('Movie Recommender System')
    # Recent searches section
    st.sidebar.title('Recent Searches')
    for search in st.session_state['state'].recent_searches:
        st.sidebar.write(search)

    selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)

        # Add selected movie to recent searches
        if selected_movie_name not in st.session_state['state'].recent_searches:
            st.session_state['state'].recent_searches.append(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])

elif selected_menu == 'All Movies':
    st.title('All Movies')
    st.subheader('List of all movies')

    num_movies = len(movies)
    num_cols = 5
    num_rows = (num_movies // num_cols) + (num_movies % num_cols > 0)

    for row in range(num_rows):
        start_index = row * num_cols
        end_index = min(start_index + num_cols, num_movies)
        row_movies = movies.iloc[start_index:end_index]

        col1, col2, col3, col4, col5 = st.columns(num_cols)

        for _, movie in row_movies.iterrows():
            with col1:
                st.text(movie['title'])
                st.image(fetch_poster(movie['movie_id']), width=120)
            col1, col2, col3, col4, col5 = col2, col3, col4, col5, None
