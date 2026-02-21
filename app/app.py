import streamlit as st
import base64

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ClashWiz",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# BACKGROUND FIX (BASE64 – WORKS ON STREAMLIT CLOUD)
# =========================================================

def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .glass {{
        background: rgba(0, 0, 0, 0.78);
        padding: 35px;
        border-radius: 20px;
        backdrop-filter: blur(6px);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.7);
    }}

    h1, h2, h3 {{
        color: #FFD700;
    }}

    .stTextInput>div>div>input {{
        background-color: rgba(255,255,255,0.1);
        color: white;
    }}

    .stSelectbox>div>div {{
        background-color: rgba(255,255,255,0.1);
        color: white;
    }}

    .stButton>button {{
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# IMPORTANT: this must exist
set_background("app/assets/background_blur.jpg")

# =========================================================
# ROYALE API IMAGE BASE (FIXED)
# =========================================================

BASE_IMAGE_URL = "https://raw.githubusercontent.com/RoyaleAPI/cr-api-assets/master/cards"

# =========================================================
# SAMPLE CARD DATA
# =========================================================

card_data = {
    "hog_rider": {"name": "Hog Rider", "category": "Troops", "elixir": 4, "rarity": "Rare"},
    "fireball": {"name": "Fireball", "category": "Spells", "elixir": 4, "rarity": "Rare"},
    "giant": {"name": "Giant", "category": "Troops", "elixir": 5, "rarity": "Rare"},
    "zap": {"name": "Zap", "category": "Spells", "elixir": 2, "rarity": "Common"},
    "baby_dragon": {"name": "Baby Dragon", "category": "Troops", "elixir": 4, "rarity": "Epic"},
    "mega_knight": {"name": "Mega Knight", "category": "Troops", "elixir": 7, "rarity": "Legendary"},
    "archers": {"name": "Archers", "category": "Troops", "elixir": 3, "rarity": "Common"},
    "goblin_barrel": {"name": "Goblin Barrel", "category": "Spells", "elixir": 3, "rarity": "Epic"},
}

card_keys = list(card_data.keys())

# =========================================================
# UI START
# =========================================================

st.markdown('<div class="glass">', unsafe_allow_html=True)

st.title("ClashWiz")
st.caption("Clash Royale Companion Interface")

st.divider()

# =========================================================
# SEARCH + FILTER
# =========================================================

col1, col2 = st.columns([2, 1])

with col1:
    search = st.text_input("Search Card")

with col2:
    category = st.selectbox(
        "Category",
        ["All", "Troops", "Spells", "Buildings"]
    )

# =========================================================
# FILTER LOGIC
# =========================================================

filtered_cards = []

for key in card_keys:
    card = card_data[key]

    if search.lower() not in card["name"].lower():
        continue

    if category != "All" and card["category"] != category:
        continue

    filtered_cards.append(key)

# =========================================================
# CARD GRID
# =========================================================

st.subheader("Cards")

cols = st.columns(4)

for i, key in enumerate(filtered_cards):
    card = card_data[key]
    image_url = f"{BASE_IMAGE_URL}/{key.replace('_','-')}.png"

    with cols[i % 4]:
        st.image(image_url, use_container_width=True)

        if st.button(card["name"], key=f"btn_{key}"):
            st.session_state.selected_card = key

# =========================================================
# CARD DETAILS
# =========================================================

if "selected_card" in st.session_state:

    selected = card_data[st.session_state.selected_card]
    detail_image_url = f"{BASE_IMAGE_URL}/{st.session_state.selected_card.replace('_','-')}.png"

    st.divider()
    st.subheader(selected["name"])
    st.image(detail_image_url, width=220)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Elixir Cost", selected["elixir"])

    with col2:
        st.metric("Rarity", selected["rarity"])

    with col3:
        st.metric("Category", selected["category"])

    st.markdown("### Win Rate")
    st.write("Coming soon from analytics.")

    st.markdown("### Hard Counters")
    st.write("Coming soon from matchup engine.")

st.markdown('</div>', unsafe_allow_html=True)
