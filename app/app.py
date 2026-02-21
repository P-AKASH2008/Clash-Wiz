import streamlit as st
import base64

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="ClashWiz",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# BACKGROUND (BASE64 FIX)
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
        padding: 30px;
        border-radius: 20px;
        backdrop-filter: blur(6px);
    }}

    h1, h2, h3 {{
        color: #FFD700;
    }}

    .stButton>button {{
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        height: 2.5em;
        font-size: 12px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background("app/assets/background_blur.jpg")

# =========================================================
# ROYALE API BASE URL
# =========================================================

BASE_IMAGE_URL = "https://raw.githubusercontent.com/RoyaleAPI/cr-api-assets/master/cards"

# =========================================================
# FULL CARD LIST (150+ CARDS)
# =========================================================

CARD_LIST = [
    "archers","arrows","baby_dragon","balloon","barbarians","barbarian_barrel",
    "battle_healer","battle_ram","bats","bomb_tower","bomber","bowler",
    "cannon","cannon_cart","clone","dark_prince","dart_goblin","earthquake",
    "electro_dragon","electro_giant","electro_spirit","elite_barbarians",
    "elixir_collector","executioner","fire_spirits","fireball","fisherman",
    "flying_machine","freeze","furnace","giant","giant_skeleton","giant_snowball",
    "goblin_barrel","goblin_cage","goblin_drill","goblin_gang","goblins",
    "golden_knight","golem","graveyard","guards","heal_spirit","hog_rider",
    "hunter","ice_golem","ice_spirit","ice_wizard","inferno_dragon","inferno_tower",
    "knight","lava_hound","lightning","little_prince","lumberjack",
    "magic_archer","mega_knight","mega_minion","miner","mini_pekka",
    "minion_horde","minions","mirror","monk","mother_witch",
    "musketeer","night_witch","pekka","phoenix","poison",
    "prince","princess","rage","ram_rider","rascals",
    "rocket","royal_delivery","royal_giant","royal_ghost","royal_hogs",
    "royal_recruits","skeleton_army","skeleton_barrel","skeleton_dragons",
    "skeleton_king","skeletons","sparky","spear_goblins","tesla",
    "the_log","three_musketeers","tornado","valkyrie","wall_breakers",
    "witch","wizard","zap","zappies"
]

# =========================================================
# UI START
# =========================================================

st.markdown('<div class="glass">', unsafe_allow_html=True)

st.title("ClashWiz")
st.caption("All Clash Royale Cards")

st.divider()

search = st.text_input("Search Card")

filtered_cards = [
    card for card in CARD_LIST
    if search.lower() in card.replace("_"," ").lower()
]

# =========================================================
# 8 CARDS PER ROW
# =========================================================

st.subheader("Cards")

cols = st.columns(8)

for i, key in enumerate(filtered_cards):

    image_url = f"{BASE_IMAGE_URL}/{key.replace('_','-')}.png"

    with cols[i % 8]:
        st.image(image_url, width=90)

        if st.button(key.replace("_"," ").title(), key=f"btn_{key}"):
            st.session_state.selected_card = key

# =========================================================
# CARD DETAILS
# =========================================================

if "selected_card" in st.session_state:

    st.divider()
    name = st.session_state.selected_card.replace("_"," ").title()
    detail_url = f"{BASE_IMAGE_URL}/{st.session_state.selected_card.replace('_','-')}.png"

    st.subheader(name)
    st.image(detail_url, width=200)

st.markdown('</div>', unsafe_allow_html=True)
