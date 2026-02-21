import streamlit as st
import json
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ClashWiz",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# BACKGROUND + GLASS UI
# --------------------------------------------------

def set_background():
    st.markdown("""
    <style>
    .stApp {
        background-image: url("app/assets/background_blur.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .glass {
        background: rgba(0, 0, 0, 0.75);
        padding: 30px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }

    h1, h2, h3 {
        color: #FFD700;
    }

    .stTextInput>div>div>input {
        background-color: rgba(255,255,255,0.1);
        color: white;
    }

    .stSelectbox>div>div {
        background-color: rgba(255,255,255,0.1);
        color: white;
    }

    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

set_background()

# --------------------------------------------------
# LOAD CARD DATA
# --------------------------------------------------

METADATA_PATH = "app/assets/card_metadata.json"
CARDS_PATH = "app/assets/cards/"

if not os.path.exists(METADATA_PATH):
    st.error("card_metadata.json not found.")
    st.stop()

with open(METADATA_PATH, "r") as f:
    card_data = json.load(f)

card_keys = list(card_data.keys())

# --------------------------------------------------
# UI START
# --------------------------------------------------

st.markdown('<div class="glass">', unsafe_allow_html=True)

st.title("ClashWiz")
st.caption("Clash Royale Companion UI")

st.divider()

# --------------------------------------------------
# SEARCH + FILTER
# --------------------------------------------------

col1, col2 = st.columns([2,1])

with col1:
    search = st.text_input("Search Card")

with col2:
    category = st.selectbox(
        "Category",
        ["All", "Troops", "Spells", "Buildings"]
    )

# --------------------------------------------------
# FILTER LOGIC
# --------------------------------------------------

filtered_cards = []

for key in card_keys:
    card = card_data[key]

    if search.lower() not in card["name"].lower():
        continue

    if category != "All" and card["category"] != category:
        continue

    filtered_cards.append(key)

# --------------------------------------------------
# CARD GRID DISPLAY
# --------------------------------------------------

st.subheader("Cards")

cols = st.columns(4)

for i, key in enumerate(filtered_cards):
    card = card_data[key]
    image_path = os.path.join(CARDS_PATH, f"{key}.png")

    with cols[i % 4]:
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)

        if st.button(card["name"], key=f"btn_{key}"):
            st.session_state.selected_card = key

# --------------------------------------------------
# CARD DETAILS PANEL
# --------------------------------------------------

if "selected_card" in st.session_state:
    selected = card_data[st.session_state.selected_card]

    st.divider()
    st.subheader(selected["name"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Elixir Cost", selected["elixir"])

    with col2:
        st.metric("Rarity", selected["rarity"])

    with col3:
        st.metric("Category", selected["category"])

    st.markdown("### Win Rate")
    st.write("Coming from analytics model...")

    st.markdown("### Hard Counters")
    st.write("Counter data will appear here.")

st.markdown('</div>', unsafe_allow_html=True)
