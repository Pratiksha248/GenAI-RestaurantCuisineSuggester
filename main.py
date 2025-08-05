import streamlit as st
import langchain_helper
from PIL import Image

# App branding setup
st.set_page_config(
    page_title="EPICURE AI",
    page_icon="🍽️",
    layout="wide"
)

# Hide Streamlit default menu, footer, and header
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Load and display logo and branding
logo = Image.open("epicureai_logo.png")  # Ensure this file exists in your working directory
col1, col2 = st.columns([1, 10])
with col1:
    st.image(logo, width=120)
with col2:
    st.markdown("""
        <h1 style='font-size: 38px; color: #fca311; font-weight: 600; margin-bottom: 0; letter-spacing: 1px;'>
        EPICURE AI
        </h1>
    """, unsafe_allow_html=True)

# Sidebar selections
cuisine = st.sidebar.selectbox("Choose Cuisine", (
    "Indian", "Italian", "Thai", "Mexican", "Chinese", "Arabic", "American", "Continental", "Beverages"
))
diet = st.sidebar.radio("Diet Preference", ("Vegan", "Non-vegan", "Mixed"))

# Main dark theme style
st.markdown("""
    <style>
        body {
            background-color: #0f1117;
        }
        .recipe-box {
            background-color: #2d2f36;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
            color: #eee;
        }
        .section-label {
            font-weight: bold;
            color: #ffd700;
        }
        .dish-card {
            border: 1px solid #333;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            background-color: #1e1f26;
            color: #eee;
        }
        .dish-name {
            font-size: 20px;
            font-weight: bold;
            color: #3dfcaa;
        }
    </style>
""", unsafe_allow_html=True)

# Run generation logic
if cuisine and diet:
    with st.spinner("✨ Generating your custom restaurant venture idea..."):
        response = langchain_helper.generate_restaurant_name_and_items(cuisine, diet)

    st.markdown(f"""### 📅 Restaurant Name: <span style='color:#00ffa2'>{response['restaurant_name']}</span>""", unsafe_allow_html=True)
    st.subheader(":bento: Top 5 Dishes")

    dishes = response.get("structured_dishes", [])

    for dish in dishes:
        name = dish.get('name', 'Unknown')
        ingredients = dish.get('ingredients', 'N/A')
        calories = dish.get('calories', 'N/A')
        recipe = dish.get('recipe', 'N/A')

        with st.container():
            st.markdown(f"""
                <div class="dish-card">
                    <div class="dish-name">{name}</div>
                    <div><span class="section-label">Ingredients used:</span> {ingredients}</div>
                    <div><span class="section-label">Calories per serving:</span> {calories}</div>
                </div>
            """, unsafe_allow_html=True)

            with st.expander("📓 Show Recipe"):
                bullets = [f"- {step.strip()}" for step in recipe.replace("\n", ". ").split(".") if step.strip()]
                st.markdown(f"""
                    <div class="recipe-box">
                        <span class="section-label">Recipe Steps:</span><br>
                        {'<br>'.join(bullets)}
                    </div>
                """, unsafe_allow_html=True)

    if "warning" in response:
        st.warning(response["warning"])