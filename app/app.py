import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv

st.set_page_config(
    page_title="Anime Recommender",
    layout="wide",
)

load_dotenv()

# -------------------------- Custom CSS Styling ---------------------------
st.markdown("""
<style>
h1 {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 1rem;
}

.block-container {
    padding-top: 2rem;
}

input[type="text"] {
    padding: 0.8rem;
    font-size: 1.1rem;
}

.result-box {
    background: #f8f9fa;
    padding: 1.2rem;
    border-radius: 10px;
    border-left: 5px solid #6c63ff;
    font-size: 1.1rem;
}

.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- Load the Pipeline ----------------------
@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline(csv_path="")

pipeline = init_pipeline()

# --------------------------- HEADER -------------------------------------
st.markdown("<h1>✨ Anime Recommender System ✨</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; font-size:1.2rem;'>"
    "Tell me what kind of anime you're in the mood for, and I’ll recommend the perfect titles!"
    "</p>",
    unsafe_allow_html=True,
)

# --------------------------- INPUT ---------------------------------------
query = st.text_input(
    "Describe what you're looking for:",
    placeholder="e.g. A dark fantasy anime like Attack on Titan",
)

# --------------------------- BUTTON --------------------------------------
recommend_btn = st.button("🎌 Recommend Anime")

# --------------------------- LOGIC ---------------------------------------
if recommend_btn:
    if not query.strip():
        st.warning("Please enter a description of your preferences first 😊")
    else:
        with st.spinner("Finding the best anime for you... 🌸"):
            try:
                recommendation = pipeline.recommend(query)

                st.markdown("<h3>🎯 Recommended Anime</h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='result-box'>{recommendation}</div>",
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")
