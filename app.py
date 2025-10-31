import streamlit as st
import requests
import pandas as pd
import urllib.parse
import os
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate

# --- CONFIGURATION & SETUP ---
# Load environment variables
load_dotenv(dotenv_path='backend/.env')
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="గడులు & గృహాలు | Fortresses & Homes",
    page_icon="🏯",
    layout="wide"
)
# Initialize Translation Client
try:
    translate_client = translate.Client()
except Exception as e:
    st.error(f"Could not initialize translation client. Ensure your Google Cloud credentials are set up correctly. Error: {e}")
    translate_client = None

# --- TRANSLATION & CACHING ---
# Dictionary for static UI text
translations = {
    "welcome_title": {"en": "Welcome to గడులు & గృహాలు", "te": "గడులు & గృహాలకు స్వాగతం"},
    "login": {"en": "Login", "te": "ప్రవేశించండి"},
    "signup": {"en": "Sign Up", "te": "నమోదు చేసుకోండి"},
    "choose_action": {"en": "Choose an action:", "te": "ఒక చర్యను ఎంచుకోండి:"},
    "username": {"en": "Username", "te": "వినియోగదారు పేరు"},
    "password": {"en": "Password", "te": "పాస్వర్డ్"},
    "choose_username": {"en": "Choose a Username", "te": "ఒక వినియోగదారు పేరును ఎంచుకోండి"},
    "choose_password": {"en": "Choose a Password", "te": "ఒక పాస్వర్డ్ను ఎంచుకోండి"},
    "logout": {"en": "Logout", "te": "నిష్క్రమించు"},
    "go_to": {"en": "Go to", "te": "ఇక్కడికి వెళ్ళండి"},
    "explore_heritage": {"en": "Explore Heritage", "te": "వారసత్వాన్ని అన్వేషించండి"},
    "submit_story": {"en": "Submit a Story", "te": "ఒక కథను సమర్పించండి"},
    "about_project": {"en": "About the Project", "te": "ప్రాజెక్ట్ గురించి"},
    "welcome_user": {"en": "Welcome, {username}!", "te": "స్వాగతం, {username}!"},
    "explore_header": {"en": "Explore Our Heritage Collection", "te": "మా వారసత్వ సేకరణను అన్వేషించండి"},
    # Add more static text translations here
}
# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en' # Default to English

# Helper function to get translated static text
def t(key):
    return translations.get(key, {}).get(st.session_state.language, f"[{key}]")
# Cached function to translate dynamic content using the API
@st.cache_data
def translate_text(text, target_language):
    if not translate_client or not text:
        return text
    try:
        result = translate_client.translate(text, target_language=target_language, source_language='en')
        return result['translatedText']
    except Exception as e:
        print(f"Translation API failed: {e}")
        return text # Return original text on failure

# --- Language Toggle Button ---
col1, col2 = st.columns([10, 1])
with col2:
    if st.toggle('తెలుగు', key='lang_toggle', value=(st.session_state.language == 'te')):
        st.session_state.language = 'te'
    else:
        st.session_state.language = 'en'

# --- DATA LOADING & AUTH FUNCTIONS (No changes needed) ---
@st.cache_data(ttl=30)
def load_data():
    try:
        response = requests.get(f"{API_URL}/places/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []

# --- AUTHENTICATION FUNCTIONS ---
def signup(username, password):
    try:
        response = requests.post(f"{API_URL}/users/", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Signup successful! Please login.")
            return True
        else:
            st.error(f"Error: {response.json().get('detail')}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")
        return False

def login(username, password):
    try:
        response = requests.post(f"{API_URL}/login", data={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error(f"Error: {response.json().get('detail')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")

# --- MAIN APP UI FUNCTION ---
def main_app():
    st.sidebar.title(t("welcome_user").format(username=st.session_state.username))
    st.sidebar.image("https://i.imgur.com/M6yB5y6.png", width=100)
    
    if st.sidebar.button(t("logout")):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

    page = st.sidebar.radio(t("go_to"), (t("explore_heritage"), t("submit_story"), t("about_project")))


    # --- Page 1: Explore Heritage ---
    if page == t("explore_heritage"):
        st.header(t("explore_header"))
        places_data = load_data()
        if not places_data:
            st.warning(translate_text("No heritage sites found. Be the first to submit one!", st.session_state.language))
        else:
            for place in places_data:
                st.markdown("---")
                # Translate dynamic content
                place_name = translate_text(place['name'], st.session_state.language)
                place_type = translate_text(place['type'], st.session_state.language)
                place_era = translate_text(place['era'], st.session_state.language)
                place_story = translate_text(place['story'], st.session_state.language)
                
                st.subheader(place["name"])
                col1, col2 = st.columns([2, 3])
                with col1:
                    image = place.get("image_url") or "https://i.imgur.com/sdVn1iA.png"
                    st.image(image, caption=f"Type: {place['type']} | Era: {place['era']}")
                with col2:
                    location_parts = [place.get('area'), place.get('region')]
                    display_location = ", ".join(filter(None, location_parts))
                    st.markdown(f"**Location:** {display_location}")
                    contributor = place.get("contributor", {})
                    st.markdown(f"**Contributor:** {contributor.get('username', 'Unknown')} {contributor.get('badge', '✨')}")
                    with st.expander("**Read the Story**"):
                        st.write(place["story"])
                    search_query = f"{place['name']}, {display_location}"
                    encoded_query = urllib.parse.quote_plus(search_query)
                    Maps_url = f"https://www.google.com/maps?q={encoded_query}"
                    st.link_button("Locate 📍", Maps_url)

    # --- Page 2: Submit a Story ---
    elif page == "Submit a Story":
        st.header("Submit a Story to the Archive")
        st.info(f"You are contributing as: **{st.session_state.username}**")

        with st.expander("✨ AI Story Assistant (Optional)"):
            st.markdown("Provide bullet points and let AI help you write the story.")
            ai_place_name = st.text_input("Name of the place (for context)", key="ai_place")
            ai_points = st.text_area("Key points (one per line)", placeholder="e.g., Built by my great-grandfather...")
            if st.button("Generate Story with AI"):
                if not ai_place_name or not ai_points:
                    st.warning("To generate a story, please enter the Place Name and at least one Key Point above.")
                else:
                    with st.spinner("AI is writing your story..."):
                        try:
                            points_list = [p.strip() for p in ai_points.split('\n') if p.strip()]
                            response = requests.post(f"{API_URL}/ai/generate-story", json={"place_name": ai_place_name, "points": points_list})
                            response.raise_for_status()
                            generated_story = response.json().get("story", "")
                            st.session_state.generated_story = generated_story
                            st.success("AI story generated! It has been placed in the text area below.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Failed to generate story: {e.response.json().get('detail')}")

        st.markdown("---")
        st.subheader("Submission Form")
        with st.form("story_form"):
            place_name = st.text_input("Name of Fortress or Home*")
            place_type = st.selectbox("Type", ["Traditional Home", "Fortress", "Haveli", "Palace"])
            area = st.text_input("Area or Locality*", placeholder="e.g., Banjara Hills")
            region = st.text_input("Region or District*", placeholder="e.g., Hyderabad")
            era = st.text_input("Era / Year Built")
            story_text = st.text_area("Your Story or Memories*", height=200, value=st.session_state.get("generated_story", ""))
            architectural_tags = st.text_input("Architectural Tags (comma-separated)", placeholder="e.g., Courtyard, Wooden Beams")
            image_url_input = st.text_input("Image URL (optional)", placeholder="https://example.com/image.jpg")
            submitted = st.form_submit_button("Submit Story to Archive")
            if submitted:
                if 'generated_story' in st.session_state:
                    del st.session_state.generated_story
                if not place_name or not region or not story_text or not area:
                    st.error("Please fill in all required fields marked with an asterisk (*).")
                else:
                    place_data = {
                        "name": place_name, "type": place_type, "area": area, "region": region,
                        "era": era, "story": story_text, "tags": architectural_tags,
                        "image_url": image_url_input,
                        "contributor_username": st.session_state.username # Use the logged-in user's name
                    }
                    try:
                        response = requests.post(f"{API_URL}/places/", json=place_data)
                        response.raise_for_status() 
                        st.success(f"Thank you! Your story about {place_name} has been submitted.")
                        st.cache_data.clear()
                        st.balloons()
                    except requests.exceptions.RequestException as e:
                        st.error(f"An error occurred while submitting: {e}")
                        if e.response: st.json(e.response.json())
    
    # --- Page 3: About ---
    elif page == "About the Project":
        st.header("About This Initiative")
        st.markdown("""
        **"గడులు & గృహాలు" (Fortresses & Traditional Homes)** is a community-driven project dedicated to preserving the rich architectural and cultural heritage of our region.
        
        This application is a fully functional platform with user accounts, AI-assisted content creation, and location-based exploration, all powered by a Python backend.
        """)


# --- LOGIN/SIGNUP ROUTING ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.title(t("welcome_title"))
    choice = st.radio(t("choose_action"), (t("login"), t("signup")))

    if choice == t("login"):
        with st.form("login_form"):
            username = st.text_input(t("username"))
            password = st.text_input(t("password"), type="password")
            if st.form_submit_button(t("login")):
                login(username, password)
    
    elif choice == t("signup"):
        with st.form("signup_form"):
            username = st.text_input(t("choose_username"))
            password = st.text_input(t("choose_password"), type="password")
            if st.form_submit_button(t("signup")):
                signup(username, password)
else:
    # A simplified main_app() is shown for brevity. You would integrate your full page logic here.
    main_app()