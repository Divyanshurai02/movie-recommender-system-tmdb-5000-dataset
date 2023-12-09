import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))

movies_listt = movies_list['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))


def f_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=200705b8080c4bc677f5d82c456ec237".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def post_vid(movie_id):
    try:
        response = requests.get(
            "https://api.themoviedb.org/3/movie/{}?api_key=200705b8080c4bc677f5d82c456ec237&append_to_response=videos".format(movie_id))
        data = response.json()
        return "https://www.youtube.com/watch?v="+data['videos']['results'][0]['key']
    except:
        return "https://www.youtube.com/results?search_query=housefull"




def movie_page(m_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=200705b8080c4bc677f5d82c456ec237&append_to_response=videos".format(
            m_id))
    data = response.json()
    return data['overview']


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    pmovie_index = movies_list[movies_list['title'] == movie].iloc[0,0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:5]
    recommended_movies = []
    poster = []
    videos = []
    n = []
    for i in movies:
        movies_id = movies_list.iloc[i[0]].movie_id
        # fetch_poster from Api
        poster.append(f_poster(movies_id))
        videos.append(post_vid(movies_id))
        n.append(movie_page(movies_id))



        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies, poster,videos,n,pmovie_index,movie



# Custom CSS styles
custom_styles = """
    <style>
        body {
            background-color: #f9f9f9;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }

        .main-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }

        .custom-title {
            color: #3498db;
            text-align: center;
            font-size: 48px;
            margin: 30px 0;
            padding: 20px;
            background-color: #3498db;
            color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }
    </style>
"""

# Display custom styles
st.markdown(custom_styles, unsafe_allow_html=True)

# Display the title with the custom style
st.markdown("<h1 class='custom-title'>Movie Recommender System</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            width: 300px;  /* You can adjust this value to set the width */
        }
    </style>
    """,
    unsafe_allow_html=True
)
with st.sidebar:
    custom_styles = """
        <style>
            body {
                background-color: #f4f4f4;
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
            }

            .main-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 15px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            }

            .custom-title {
                color: #e74c3c;
                text-align: center;
                font-size: 48px;
                margin: 20px 0;
                padding: 15px;
                background-color: #2c3e50;
                color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            }
        </style>
    """
    st.markdown("<h1 class='custom-title'>Select Movie I will Predict the Next 4 Similar Movies</h1>", unsafe_allow_html=True)

    selected_movie_name=st.selectbox(" ",
    (movies_listt)
)
names, pictures,videos,n,m,movie_name= recommend(selected_movie_name)
if 'clicked_sidebar' not in st.session_state:
    st.session_state.clicked_sidebar = -1
with st.sidebar:
    if st.toggle("predict"):
        names, pictures,videos,n,m,movie= recommend(selected_movie_name)
        col1, col2 = st.columns(2,gap="small")

        # Create a column

        with col1:
            st.subheader(names[0])
            image_url = "https://image.tmdb.org/t/p/w500/" + pictures[0]
            # Assuming you have a link URL you want to navigate to
            link_url = videos[0]

            # Use HTML to create a clickable image with a link
            html_code = f"<a href='{link_url}' target='_blank'><img src='{image_url}' alt='Clickable Image' style='width: 230px; height: 400px;'></a>"

            # Display the HTML code in Streamlit
            st.markdown(html_code, unsafe_allow_html=True)
            if st.button(names[0]+" Trailer"):
                st.session_state.clicked_sidebar = 0

            # Check if the image is clicked (you can use a session state variable if needed)
        # Additional logic can be added below if needed

        with col2:
            st.subheader(names[1])
            image_url = "https://image.tmdb.org/t/p/w500/" + pictures[1]
            # Assuming you have a link URL you want to navigate to
            link_url = videos[1]

            # Use HTML to create a clickable image with a link
            html_code = f"<a href='{link_url}' target='_blank'><img src='{image_url}' alt='Clickable Image' style='width: 230px; height: 400px;'></a>"

            # Display the HTML code in Streamlit
            st.markdown(html_code, unsafe_allow_html=True)
            if st.button(names[1]+" Trailer"):
                st.session_state.clicked_sidebar = 1
        col3, col4= st.columns(2, gap="small")

        with col3:
            st.subheader(names[2])
            image_url = "https://image.tmdb.org/t/p/w500/" + pictures[2]
            # Assuming you have a link URL you want to navigate to
            link_url = videos[2]

            # Use HTML to create a clickable image with a link
            html_code = f"<a href='{link_url}' target='_blank'><img src='{image_url}' alt='Clickable Image' style='width: 230px; height: 400px;'></a>"

            # Display the HTML code in Streamlit
            st.markdown(html_code, unsafe_allow_html=True)
            if st.button(names[2]+" Trailer"):
                st.session_state.clicked_sidebar = 2
        with col4:
            st.subheader(names[3])
            image_url = "https://image.tmdb.org/t/p/w500/" + pictures[3]
            # Assuming you have a link URL you want to navigate to
            link_url = videos[3]

            # Use HTML to create a clickable image with a link
            html_code = f"<a href='{link_url}' target='_blank'><img src='{image_url}' alt='Clickable Image' style='width: 230px; height: 400px;'></a>"

            # Display the HTML code in Streamlit
            st.markdown(html_code, unsafe_allow_html=True)
            if st.button(names[3]+" Trailer"):
                st.session_state.clicked_sidebar = 3

# Initialize session state

# Display the result outside the sidebar based on the click event
if st.session_state.clicked_sidebar==-1:
    cl1,cl2 = st.columns(2,gap='small')
    with cl1:
        st.header(movie_name)
        st.markdown("(selected Movie for Prediction)")
        st.image(f_poster(m),width=250)
    with cl2:
        v = movie_page(m)

        # Write text using HTML in Streamlit
        styled_html_text = f"""
                   <style>
                     body {{
                       font-family: 'Arial', sans-serif;
                       background-color: #f0f0f0;
                       margin: 0;
                       padding: 20px;
                     }}

                     .container {{
                       max-width: 800px;
                       margin: 0 auto;
                       background-color: #fff;
                       padding: 20px;
                       border-radius: 10px;
                       box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                     }}

                     h6 {{
                       color: #3498db;
                       font-size: 24px;
                       margin-bottom: 10px;
                     }}

                     p {{
                       font-size: 18px;
                       color: #2c3e50;
                       line-height: 1.6;
                     }}
                   </style>

                   <div class="container">
                       <h6>Overview</h6>
                       <p>{v}</p>
                   </div>
                   """

        # Display HTML-rendered text with custom styles in Streamlit
        st.markdown(styled_html_text, unsafe_allow_html=True)
    with st.expander("Watch Trailer"):
        st.video(post_vid(m))
elif st.session_state.clicked_sidebar==0:
    cl1, cl2 = st.columns(2, gap='small')
    with cl1:
        st.subheader(names[0])
        st.image(pictures[0], width=250)
    with cl2:
        v = n[0]

        # Write text using HTML in Streamlit
        styled_html_text = f"""
                   <style>
                     body {{
                       font-family: 'Arial', sans-serif;
                       background-color: #f0f0f0;
                       margin: 0;
                       padding: 20px;
                     }}

                     .container {{
                       max-width: 800px;
                       margin: 0 auto;
                       background-color: #fff;
                       padding: 20px;
                       border-radius: 10px;
                       box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                     }}

                     h6 {{
                       color: #3498db;
                       font-size: 24px;
                       margin-bottom: 10px;
                     }}

                     p {{
                       font-size: 18px;
                       color: #2c3e50;
                       line-height: 1.6;
                     }}
                   </style>

                   <div class="container">
                       <h6>Overview</h6>
                       <p>{v}</p>
                   </div>
                   """

        # Display HTML-rendered text with custom styles in Streamlit
        st.markdown(styled_html_text, unsafe_allow_html=True)
    with st.expander("Watch Trailer"):
        st.video(videos[0])
# for movie 2nd
elif st.session_state.clicked_sidebar==1:
    cl1, cl2 = st.columns(2, gap='small')
    with cl1:
        st.subheader(names[1])
        st.image(pictures[1], width=250)
    with cl2:
        v = n[1]

        styled_html_text = f"""
                   <style>
                     body {{
                       font-family: 'Arial', sans-serif;
                       background-color: #f0f0f0;
                       margin: 0;
                       padding: 20px;
                     }}

                     .container {{
                       max-width: 800px;
                       margin: 0 auto;
                       background-color: #fff;
                       padding: 20px;
                       border-radius: 10px;
                       box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                     }}

                     h6 {{
                       color: #3498db;
                       font-size: 24px;
                       margin-bottom: 10px;
                     }}

                     p {{
                       font-size: 18px;
                       color: #2c3e50;
                       line-height: 1.6;
                     }}
                   </style>

                   <div class="container">
                       <h6>Overview</h6>
                       <p>{v}</p>
                   </div>
                   """

        # Display HTML-rendered text with custom styles in Streamlit
        st.markdown(styled_html_text, unsafe_allow_html=True)
    with st.expander("Watch Trailer"):
        st.video(videos[1])
# for movie 3rd
elif st.session_state.clicked_sidebar==2:
    cl1, cl2 = st.columns(2, gap='small')
    with cl1:
        st.subheader(names[2])
        st.image(pictures[2], width=250)
    with cl2:
        v = n[2]

        # Write text using HTML in Streamlit
        styled_html_text = f"""
                   <style>
                     body {{
                       font-family: 'Arial', sans-serif;
                       background-color: #f0f0f0;
                       margin: 0;
                       padding: 20px;
                     }}

                     .container {{
                       max-width: 800px;
                       margin: 0 auto;
                       background-color: #fff;
                       padding: 20px;
                       border-radius: 10px;
                       box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                     }}

                     h6 {{
                       color: #3498db;
                       font-size: 24px;
                       margin-bottom: 10px;
                     }}

                     p {{
                       font-size: 18px;
                       color: #2c3e50;
                       line-height: 1.6;
                     }}
                   </style>

                   <div class="container">
                       <h6>Overview</h6>
                       <p>{v}</p>
                   </div>
                   """

        # Display HTML-rendered text with custom styles in Streamlit
        st.markdown(styled_html_text, unsafe_allow_html=True)
    with st.expander("Watch Trailer"):
        st.video(videos[2])
# for movies 4th
elif st.session_state.clicked_sidebar==3:
    cl1, cl2 = st.columns(2, gap='small')
    with cl1:
        st.subheader(names[3])
        st.image(pictures[3], width=250)
    with cl2:
        v = n[3]

        # Your HTML content with inline CSS styles
        styled_html_text = f"""
           <style>
             body {{
               font-family: 'Arial', sans-serif;
               background-color: #f0f0f0;
               margin: 0;
               padding: 20px;
             }}

             .container {{
               max-width: 800px;
               margin: 0 auto;
               background-color: #fff;
               padding: 20px;
               border-radius: 10px;
               box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
             }}

             h6 {{
               color: #3498db;
               font-size: 24px;
               margin-bottom: 10px;
             }}

             p {{
               font-size: 18px;
               color: #2c3e50;
               line-height: 1.6;
             }}
           </style>

           <div class="container">
               <h6>Overview</h6>
               <p>{v}</p>
           </div>
           """

        # Display HTML-rendered text with custom styles in Streamlit
        st.markdown(styled_html_text, unsafe_allow_html=True)

    with st.expander("Watch Trailer"):
        st.video(videos[3])



custom_styles = """
    <style>
        body {
            background-color: #f9f9f9;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }

        .made-by-container {
            text-align: center;
            margin-top: 20px;
        }

        .made-by-text {
            color: #3498db;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 1px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
    </style>
"""

# Display custom styles
st.markdown(custom_styles, unsafe_allow_html=True)

# Display the "made by Divyanshu Rai" text with the custom style
st.markdown("<div class='made-by-container'><p class='made-by-text'>Made by Divyanshu Rai</p></div>", unsafe_allow_html=True)


