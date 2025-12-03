import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv


st.set_page_config(page_title="Anime Recommender", layout="wide")

load_dotenv()

@st.cache_resource
def init_pipeline():
    pipeline = AnimeRecommendationPipeline(csv_path="")
    return pipeline

pipeline = init_pipeline()

st.title("Anime Recommender System")
query = st.text_input("Enter your anime preferences:e.g a light hearted anime with adventure and fantasy elements")
if query:
    with st.spinner("Generating recommendations..."):
        try:
            recommendation = pipeline.recommend(query)
            st.subheader("Recommended Anime:")
            st.write(recommendation)
        except Exception as e:
            st.error(f"An error occurred: {e}")
