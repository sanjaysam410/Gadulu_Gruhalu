import streamlit as st
from datetime import datetime
import os
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="గడులు & గృహాలు | Fortresses & Homes",
    page_icon="🏯",
    layout="wide"
)

# --- Simulating a Database using Session State ---
# This initializes the 'database' only once per session.
def initialize_database():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        # Simulates the 'Users' table
        st.session_state.users = {
            "s_rao": {"name": "S. Rao", "contributions": 2, "badge": "Heritage Keeper 🏅"},
            "priya_k": {"name": "Priya K.", "contributions": 1, "badge": "Storyteller 📖"},
            "admin": {"name": "Admin", "contributions": 0, "badge": "Curator 🏛️"}
        }
        
        # Load places from JSON if exists, else use default
        if os.path.exists("stories.json"):
            try:
                with open("stories.json", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        st.session_state.places = json.loads(content)
                    else:
                        raise ValueError("Empty file")
            except (json.JSONDecodeError, ValueError):
                # If file is empty or invalid, fall back to default and recreate file
                st.session_state.places = {
                    "wgl_fort": {
                        "name": "Warangal Fort (వరంగల్ కోట)",
                        "type": "Fortress",
                        "region": "Warangal",
                        "era": "12th Century CE",
                        "contributor_id": "s_rao",
                        "image": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Warangal_Fort_Entrance.jpg",
                        "story": "The fort was the capital of the Kakatiya dynasty. The intricate stone gateways, known as Kakatiya Kala Thoranam, are an architectural marvel and have become a symbol of Telangana.",
                        "tags": ["Kakatiya", "Stone Archway", "Archaeology"],
                        "comments": [
                            {"user": "Priya K.", "text": "The detail on the arches is incredible!"}
                        ]
                    },
                    "chowmahalla": {
                        "name": "Chowmahalla Palace (చౌమహల్లా ప్యాలెస్)",
                        "type": "Traditional Home (Palace)",
                        "region": "Hyderabad",
                        "era": "18th-19th Century CE",
                        "contributor_id": "priya_k",
                        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Chowmahalla_Palace_Hyderabad_India.jpg/1280px-Chowmahalla_Palace_Hyderabad_India.jpg",
                        "story": "This was the seat of the Asaf Jahi dynasty and the official residence of the Nizams of Hyderabad. Its name means 'Four Palaces'. The grand Khilwat Mubarak hall is breathtaking.",
                        "tags": ["Nizam", "Courtyard", "Palace"],
                        "comments": []
                    },
                }
                with open("stories.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state.places, f, ensure_ascii=False, indent=2)
        else:
            # Simulates the 'Homes' and 'Forts' tables with stories
            st.session_state.places = {
                "wgl_fort": {
                    "name": "Warangal Fort (వరంగల్ కోట)",
                    "type": "Fortress",
                    "region": "Warangal",
                    "era": "12th Century CE",
                    "contributor_id": "s_rao",
                    "image": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Warangal_Fort_Entrance.jpg",
                    "story": "The fort was the capital of the Kakatiya dynasty. The intricate stone gateways, known as Kakatiya Kala Thoranam, are an architectural marvel and have become a symbol of Telangana.",
                    "tags": ["Kakatiya", "Stone Archway", "Archaeology"],
                    "comments": [
                        {"user": "Priya K.", "text": "The detail on the arches is incredible!"}
                    ]
                },
                "chowmahalla": {
                    "name": "Chowmahalla Palace (చౌమహల్లా ప్యాలెస్)",
                    "type": "Traditional Home (Palace)",
                    "region": "Hyderabad",
                    "era": "18th-19th Century CE",
                    "contributor_id": "priya_k",
                    "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Chowmahalla_Palace_Hyderabad_India.jpg/1280px-Chowmahalla_Palace_Hyderabad_India.jpg",
                    "story": "This was the seat of the Asaf Jahi dynasty and the official residence of the Nizams of Hyderabad. Its name means 'Four Palaces'. The grand Khilwat Mubarak hall is breathtaking.",
                    "tags": ["Nizam", "Courtyard", "Palace"],
                    "comments": []
                },
            }

# --- Main Application ---

# Initialize the 'database' on first run
initialize_database()

# --- Header and Title ---
st.title("గడులు & గృహాలు | Fortresses & Traditional Homes")
st.markdown("A living archive to preserve our cultural heritage.")

# --- Sidebar for Navigation & User Simulation ---
st.sidebar.image("https://i.imgur.com/M6yB5y6.png", width=100) # Placeholder Logo
st.sidebar.title("Navigation")

# Simple user simulation - no real authentication
username_input = st.sidebar.text_input("Enter your name to contribute:", "Guest")
if username_input not in st.session_state.users:
    st.session_state.users[username_input.lower()] = {"name": username_input, "contributions": 0, "badge": "New Contributor ✨"}

# Navigation Radio Buttons
page = st.sidebar.radio(
    "Go to",
    ("Explore Heritage", "Submit a Story", "About the Project")
)
st.sidebar.markdown("---")
st.sidebar.info("This is a prototype. Data is not saved permanently.")


# ==============================================================================
#                             PAGE 1: EXPLORE HERITAGE
# ==============================================================================
if page == "Explore Heritage":
    st.header("Explore Our Heritage Collection")

    # --- Filtering Controls ---
    col1, col2, col3 = st.columns(3)
    with col1:
        regions = ["All"] + list(set(p["region"] for p in st.session_state.places.values()))
        selected_region = st.selectbox("Filter by Region:", regions)
    with col2:
        types = ["All"] + list(set(p["type"] for p in st.session_state.places.values()))
        selected_type = st.selectbox("Filter by Type:", types)
    with col3:
        search_query = st.text_input("Search by Name or Tag:")

    # --- Filtering Logic ---
    filtered_places = st.session_state.places.values()
    if selected_region != "All":
        filtered_places = [p for p in filtered_places if p["region"] == selected_region]
    if selected_type != "All":
        filtered_places = [p for p in filtered_places if p["type"] == selected_type]
    if search_query:
        query = search_query.lower()
        filtered_places = [p for p in filtered_places if query in p["name"].lower() or any(query in tag.lower() for tag in p["tags"])]

    # --- Displaying Data (UI Wireframe Implementation) ---
    if not filtered_places:
        st.warning("No entries match your criteria.")
    else:
        for place in filtered_places:
            contributor = st.session_state.users.get(place["contributor_id"], {"name": "Unknown", "badge": ""})
            
            st.markdown("---")
            st.subheader(place["name"])
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.image(place["image"], caption=f"Type: {place['type']} | Era: {place['era']}")

            with col2:
                st.markdown(f"**Location:** {place['region']}")
                st.markdown(f"**Contributor:** {contributor['name']} {contributor['badge']}")
                
                with st.expander("**Read the Story**"):
                    st.write(place["story"])
                
                tags_html = " ".join([f"`{tag}`" for tag in place["tags"]])
                st.markdown(f"**Tags:** {tags_html}")

                # Comments and Reactions simulation
                st.write("**Community Reactions:**")
                if place['comments']:
                    for comment in place['comments']:
                        st.caption(f"💬 {comment['user']}: \"{comment['text']}\"")
                else:
                    st.caption("No comments yet.")
                
                c1, c2, c3, c4 = st.columns(4)
                c1.button("❤️ Like", key=f"like_{place['name']}")
                c2.button("👍 Agree", key=f"agree_{place['name']}")
                c3.button("🤔 Insightful", key=f"insight_{place['name']}")


# ==============================================================================
#                             PAGE 2: SUBMIT A STORY
# ==============================================================================
elif page == "Submit a Story":
    st.header("Submit a Story to the Archive")
    st.info(f"You are contributing as: **{username_input}**")

    # --- Submission Form (UI Wireframe Implementation) ---
    with st.form("story_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            place_name = st.text_input("Name of Fortress or Home (e.g., Gadwal Fort)", key="place_name")
            place_type = st.selectbox("Type", ["Traditional Home", "Fortress", "Haveli", "Palace","Temples","Mosques","Churches","Other"], key="place_type")
        with col2:
            place_region = st.text_input("Region or District (e.g., Mahbubnagar)", key="place_region")
            place_era = st.text_input("Era / Year Built (e.g., 17th Century)", key="place_era")

        # --- Multimedia Upload ---
        uploaded_images = st.file_uploader(
            "Upload Photos (you can select multiple)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="images"
        )

        # --- Story Input (Free-form vs. Structured) ---
        story_input_method = st.radio("Choose input method:", ["Write Story", "AI Story Assistant (Demo)"])
        
        if story_input_method == "Write Story":
            story_text = st.text_area("Your Story or Memories", height=200, key="story_text",
                                      placeholder="Share details about the architecture, family history, or any special memories...")
        else:
            story_points = st.text_area("AI Story Assistant: List key points (one per line)", height=150,
                                        placeholder="e.g., Built by my great-grandfather\nKnown for its large wooden doors\nWe used to play in the central courtyard")
            story_text = "" # Placeholder for AI generated text

        architectural_tags = st.text_input("Architectural Tags (comma-separated)", 
                                           placeholder="e.g., Courtyard, Wooden Beams, Arches")
        
        # --- Volunteer Help ---
        request_help = st.checkbox("I need help from a volunteer to complete this story.")

        # --- Form Submission ---
        submitted = st.form_submit_button("Submit Story to Archive")

        if submitted:
            if not place_name or not story_text and not story_points:
                st.error("Please fill in at least the name and the story/key points.")
            else:
                # Process and "save" the data to the session state
                place_id = place_name.lower().replace(" ", "_")
                
                # Simple AI demo
                if story_input_method == "AI Story Assistant (Demo)" and story_points:
                    points = story_points.split('\n')
                    story_text = "This historic place holds deep significance. " + " ".join(points) + ". These memories paint a vivid picture of its past."

                st.session_state.places[place_id] = {
                    "name": place_name,
                    "type": place_type,
                    "region": place_region,
                    "era": place_era,
                    "contributor_id": username_input.lower(),
                    "image": "https://i.imgur.com/sdVn1iA.png", # Placeholder for uploaded image
                    "story": story_text,
                    "tags": [tag.strip() for tag in architectural_tags.split(',')] if architectural_tags else [],
                    "comments": []
                }
                
                # Update contributor stats
                st.session_state.users[username_input.lower()]["contributions"] += 1
                
                # --- Save to JSON file ---
                with open("stories.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state.places, f, ensure_ascii=False, indent=2)
                
                st.success(f"Thank you, {username_input}! Your story about {place_name} has been submitted for review.")
                st.balloons()
                if request_help:
                    st.info("A volunteer will be notified to assist you. Thank you for your contribution!")

# ==============================================================================
#                             PAGE 3: ABOUT
# ==============================================================================
elif page == "About the Project":
    st.header("About This Initiative")
    st.markdown("""
    **"గడులు & గృహాలు" (Fortresses & Traditional Homes)** is a community-driven project dedicated to preserving the rich architectural and cultural heritage of our region.
    
    ### Our Mission
    - **Document:** To create a comprehensive digital record of historic structures.
    - **Narrate:** To capture the human stories, lifestyles, and memories associated with these places.
    - **Connect:** To build a bridge between generations and connect a global audience to our local heritage.
    
    ### Why This Matters
    Many of these structures and the stories they hold are at risk of being lost. This platform serves as a **living archive**, ensuring that the legacy of our ancestors is preserved and celebrated for years to come.
    
    **This application is an interactive prototype.** It demonstrates the core functionality envisioned for the final platform, including community submissions and heritage exploration.
    """)