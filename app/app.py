import streamlit as st
import base64
import requests

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="ClashWiz",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# BACKGROUND
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
        background: rgba(0, 0, 0, 0.80);
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
        font-size: 11px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background("app/assets/background_blur.jpg")

# =========================================================
# FETCH ALL CARDS FROM ROYALEAPI
# =========================================================

@st.cache_data
def fetch_all_cards():
    url = "https://api.github.com/repos/RoyaleAPI/cr-api-assets/contents/cards-150-gold"
    response = requests.get(url)
    data = response.json()

    card_names = []
    for file in data:
        if file["name"].endswith(".png"):
            card_names.append(file["name"].replace(".png",""))

    return sorted(card_names)

CARD_LIST = fetch_all_cards()

BASE_IMAGE_URL = "https://raw.githubusercontent.com/RoyaleAPI/cr-api-assets/master/cards-150-gold"

# =========================================================
# UI
# =========================================================

st.markdown('<div class="glass">', unsafe_allow_html=True)

st.title("ClashWiz")
st.caption("All Clash Royale Cards + Evolutions")

st.divider()

search = st.text_input("Search Card")

filtered_cards = [
    card for card in CARD_LIST
    if search.lower() in card.replace("-"," ").lower()
]

# =========================================================
# DISPLAY 8 PER ROW
# =========================================================

st.subheader(f"{len(filtered_cards)} Cards Found")

cols = st.columns(8)

for i, key in enumerate(filtered_cards):

    image_url = f"{BASE_IMAGE_URL}/{key}.png"

    with cols[i % 8]:
        st.image(image_url, width=90)

        if st.button(key.replace("-"," ").title(), key=f"btn_{key}"):
            st.session_state.selected_card = key

# =========================================================
# CARD DETAIL
# =========================================================

if "selected_card" in st.session_state:

    st.divider()
    name = st.session_state.selected_card.replace("-"," ").title()
    detail_url = f"{BASE_IMAGE_URL}/{st.session_state.selected_card}.png"

    st.subheader(name)
    st.image(detail_url, width=220)

st.markdown('</div>', unsafe_allow_html=True)
