import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ClashWiz",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 🔥 PUT YOUR ROYALE API PERMALINK COMMIT HASH HERE
# =========================================================

ROYALE_COMMIT = "PUT_YOUR_COMMIT_HASH_HERE"
BASE_IMAGE_URL = f"https://raw.githubusercontent.com/RoyaleAPI/cr-api-assets/{ROYALE_COMMIT}/cards"

# =========================================================
# BACKGROUND + GLASS THEME
# =========================================================

st.markdown("""
<style>
.stApp {
    background-image: url("app/assets/background_blur.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.glass {
    background: rgba(0, 0, 0, 0.72);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(6px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
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

# =========================================================
# SAMPLE CARD DATA (expand later or load dynamically)
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
# MAIN UI
# =========================================================

st.markdown('<div class="glass">', unsafe_allow_html=True)

st.title("ClashWiz")
st.caption("Clash Royale Companion Interface")

st.divider()

# =========================================================
# SEARCH + FILTER
# =========================================================

col1, col2 = st.columns([2,1])

with col1:
    search = st.text_input("Search Card")

with col2:
    category = st.selectbox(
        "Category",
        ["All", "Troops", "Spells", "Buildings"]
    )

# =========================================================
# FILTER CARDS
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
# CARD GRID DISPLAY
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
# CARD DETAIL PANEL
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
    st.write("Will connect to analytics model.")

    st.markdown("### Hard Counters")
    st.write("Will connect to matchup engine.")

st.markdown('</div>', unsafe_allow_html=True)
