import streamlit as st
import pandas as pd
import random
import time
import base64
import numpy as np

# --- 1. AESTHETIC CONFIGURATION & CUSTOM CSS (Colorful/Aesthetic) ---
st.set_page_config(
    page_title="Aesthetic AI Video Editor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a dark, vibrant, and aesthetic look (inspired by 'Dopamine Colors' design)
st.markdown("""
<style>
    /* Main Streamlit container background */
    .stApp {
        background-color: #121212; /* Darker background */
        color: #E0E0E0;
    }
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 3rem;
    }
    /* Header and Title Styling */
    h1 {
        color: #FF6B6B; /* Vibrant Coral */
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    h2, h3 {
        color: #4ECDC4; /* Teal Accent */
        font-family: 'Inter', sans-serif;
    }
    /* Customize buttons */
    div.stButton > button {
        background-color: #FF6B6B; /* Coral */
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.2s ease-in-out;
        border: 2px solid #FF6B6B;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    div.stButton > button:hover {
        background-color: #E63946; /* Slightly darker coral */
        border-color: #E63946;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
    }
    /* Input Fields */
    .stTextInput, .stTextArea, .stFileUploader {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #333333;
    }
    /* Checkboxes/Radio buttons/Sliders */
    .stRadio > label, .stCheckbox > label, .stSlider > div > div {
        color: #E0E0E0;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    .css-1lcbmhc {
        color: #4ECDC4;
    }
    /* Message Box for Recommendations/Summary */
    .result-box {
        border-left: 5px solid #4ECDC4; /* Teal Accent */
        background-color: #1E1E1E;
        padding: 15px;
        margin-top: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    .music-box {
        border-left: 5px solid #FFC300; /* Gold Accent */
    }
</style>
""", unsafe_allow_html=True)

# --- 2. KAGGLE DATASET MOCK (AI-Powered Music Recommendation System) ---
# Mocking a Kaggle dataset structure linking Sentiment to Music attributes.
# Source: AI-Powered Music Recommendation System - Kaggle (Conceptual Dataset)
MOCK_KAGGLE_MUSIC_DATA = [
    {"Mood": "Joyful", "Song_Name": "Electric Sunrise", "Artist": "Neon Dreams", "Genre": "Synthpop", "Tempo_BPM": 128},
    {"Mood": "Energetic", "Song_Name": "The Ascent", "Artist": "Apex Sound", "Genre": "Trance", "Tempo_BPM": 140},
    {"Mood": "Melancholic", "Song_Name": "Faded Hues", "Artist": "Rainy Days", "Genre": "Ambient", "Tempo_BPM": 65},
    {"Mood": "Calm", "Song_Name": "Forest Walk", "Artist": "Lofi Panda", "Genre": "Lo-fi", "Tempo_BPM": 80},
    {"Mood": "Epic", "Song_Name": "Echoes of Glory", "Artist": "Cinematic Orchestra", "Genre": "Orchestral", "Tempo_BPM": 90},
    {"Mood": "Neutral", "Song_Name": "Background Loop 1", "Artist": "Studio Tools", "Genre": "Instrumental", "Tempo_BPM": 100},
]
MUSIC_DF = pd.DataFrame(MOCK_KAGGLE_MUSIC_DATA)

# --- 3. CORE AI/VIDEO PROCESSING LOGIC (SIMULATED) ---

def generate_summary_and_mood(video_file, prompt):
    """Simulates LLM-based video transcription/summary generation."""
    if not video_file:
        return None, None
    
    # Simulate processing time
    time.sleep(1)
    
    # Mock analysis based on the uploaded file type and user prompt
    if "tutorial" in prompt.lower() or "how-to" in video_file.name.lower():
        summary = "The video is a concise step-by-step tutorial on Python web scraping using the BeautifulSoup library. Key steps covered include installation, making an HTTP request, and parsing HTML tags."
        mood = "Informative"
    elif "travel" in prompt.lower() or "vlog" in video_file.name.lower():
        summary = "A travel vlog documenting a trip to Kyoto, focusing on serene temple visits and vibrant market scenes. The highlights are the Fushimi Inari Shrine and Nishiki Market food tour."
        mood = "Joyful"
    else:
        summary = "This is a generic content summary focusing on the general theme. It appears to be a mixed-media piece requiring conversational editing instructions."
        mood = "Neutral"

    return summary, mood

def recommend_music(mood):
    """Uses the mock Kaggle dataset to recommend a song based on video mood."""
    mood_map = {
        "Joyful": ["Joyful", "Energetic"],
        "Informative": ["Calm", "Neutral"],
        "Melancholic": ["Melancholic"],
        "Neutral": ["Neutral", "Calm", "Epic"],
        "Energetic": ["Energetic", "Joyful"]
    }
    
    possible_moods = mood_map.get(mood, ["Neutral"])
    
    recommendations = MUSIC_DF[MUSIC_DF['Mood'].isin(possible_moods)].copy()
    
    if recommendations.empty:
        # Fallback to a neutral track if specific mood search fails
        recommendations = MUSIC_DF[MUSIC_DF['Mood'] == "Neutral"].copy()
        
    # Select a random recommendation from the filtered list
    recommended_song = recommendations.sample(n=1).iloc[0]
    
    song_details = (
        f"**Song:** {recommended_song['Song_Name']} by {recommended_song['Artist']}\n"
        f"**Genre:** {recommended_song['Genre']} | **Tempo:** {recommended_song['Tempo_BPM']} BPM\n"
        f"**Mood Match:** {recommended_song['Mood']}\n"
    )
    return f"Based on the video's mood ('{mood}'), I recommend the following song:", song_details

def simulate_video_processing(video_file, config):
    """Simulates the core video editing process based on user configuration."""
    if not video_file:
        return None
    
    # Simulate creating a binary file for download
    # In a real app, this would be the output video file
    data = b'This is a placeholder for your processed video file.'
    
    # Generate a descriptive message about the edits made
    edits = []
    
    # 1. Custom Prompt Edits (Transition/Brightness Control)
    if config['prompt']:
        # This addresses the automatic transition control and brightness requirement
        edits.append(f"AI applied custom edits based on the prompt: '{config['prompt']}'. This likely included **automatic transition control** (e.g., cross-dissolves on scene changes) and **brightness/color-grade adjustments** to match the desired tone.")

    # 2. Aspect Ratio & Resolution
    if config['aspect_ratio'] != "Original":
        edits.append(f"Aspect Ratio adjusted to: **{config['aspect_ratio']}**.")
    if config['resolution'] != "Original":
        edits.append(f"Resolution set to: **{config['resolution']}**.")
        
    # 3. Subtitles
    if config['subtitles']:
        edits.append("**Automatic Subtitles** generated and burned into the video. (Mocked content: 'Hello, this is the first subtitle.')")

    # 4. Music
    if config['music']:
        edits.append("Music recommendation applied (see recommendation details).")
        
    
    edit_summary = "\n- " + "\n- ".join(edits)
    
    return data, edit_summary

# --- 4. STREAMLIT UI LAYOUT ---

st.title("🎬 Aesthetic AI Video & Audio Editor")
st.markdown("---")

st.markdown(
    """
    <p style='font-size: 1.2rem; color: #E0E0E0;'>
        Welcome to the Aesthetic AI Editor! Upload your media and tell the AI what you need.
    </p>
    """, unsafe_allow_html=True
)

# Initialize Session State for conversational memory
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'mood' not in st.session_state:
    st.session_state.mood = None
if 'music_rec' not in st.session_state:
    st.session_state.music_rec = None
if 'music_details' not in st.session_state:
    st.session_state.music_details = None

# --- File Uploader (Video and Audio Input) ---
uploaded_file = st.file_uploader(
    "Upload Video (MP4, MOV) or Audio (MP3, WAV)", 
    type=["mp4", "mov", "mp3", "wav"],
    key="file_uploader"
)

st.markdown("---")

if uploaded_file is not None:
    st.success(f"File uploaded successfully: **{uploaded_file.name}**")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        # Display video/audio preview 
        st.subheader("Preview Media")
        if uploaded_file.type.startswith('video'):
            st.video(uploaded_file, format='video/mp4', start_time=0)
        elif uploaded_file.type.startswith('audio'):
            st.audio(uploaded_file, format='audio/wav')
        else:
            st.warning("File preview not available.")
            
        # --- Resolution Options ---
        st.subheader("Video Quality Options")
        resolution = st.selectbox(
            "Select Output Resolution",
            ["Original", "1080p (1920x1080)", "720p (1280x720)", "480p (854x480)"],
            key="resolution_select"
        )
        
    with col2:
        st.subheader("AI Editing Features")
        
        # --- Conversational Feature Checkboxes ---
        st.markdown(
            """
            <p style='font-weight: bold; color: #E0E0E0;'>
                Check the features you would like the AI to handle:
            </p>
            """, unsafe_allow_html=True
        )

        # Feature: Summary/Highlight (Automatically runs to determine mood)
        st.checkbox("Generate Video Summary and Highlights", value=True, disabled=True, key="feat_summary", help="This analysis is required to determine the video's mood.")

        # Feature: Subtitles (If needed)
        subtitles_needed = st.checkbox(
            "Generate and Add Subtitles", 
            value=False, 
            key="feat_subtitles",
            help="Automatically transcribe the audio and burn subtitles onto the video."
        )

        # Feature: Music Recommendation (If needed)
        music_needed = st.checkbox(
            "Get Mood-Based Music Recommendation (Uses mock Kaggle data)", 
            value=False, 
            key="feat_music",
            help="AI will analyze the video's mood/summary and suggest a suitable song from the mock dataset."
        )

        st.markdown("---")
        
        # Feature: Automatic Transition, Brightness Control, and Aspect Ratio
        st.subheader("Creative Controls (Prompt-Based)")
        
        # Aspect Ratio Input
        aspect_ratio = st.selectbox(
            "Adjust Aspect Ratio",
            ["Original", "16:9 (Widescreen)", "4:3 (Classic)", "9:16 (Vertical)"],
            key="aspect_ratio_select"
        )

        # Prompt for controlling brightness and transitions
        user_prompt = st.text_area(
            "**AI Prompt for Editing:** (e.g., 'Make the transitions smooth and cinematic, and increase brightness for a vibrant, sunny feel.')",
            key="editing_prompt",
            placeholder="Describe the aesthetic and mood you want (e.g., 'Add fast cuts with glitch transitions, and use a dark, moody color grade to reduce brightness.')"
        )
        
        if st.button("Start AI Processing", key="process_button"):
            
            # 1. Run AI Analysis (Summary & Mood)
            with st.spinner('Analyzing video content for summary and mood...'):
                summary, mood = generate_summary_and_mood(uploaded_file, user_prompt)
                st.session_state.summary = summary
                st.session_state.mood = mood
                st.session_state.music_rec = None
                st.session_state.music_details = None
            
            # 2. Handle Music Recommendation
            if music_needed and mood:
                with st.spinner('Matching video mood to the Kaggle Music Database...'):
                    rec_message, rec_details = recommend_music(mood)
                    st.session_state.music_rec = rec_message
                    st.session_state.music_details = rec_details
            
            # 3. Compile Configuration
            config = {
                'prompt': user_prompt,
                'aspect_ratio': aspect_ratio,
                'resolution': resolution,
                'subtitles': subtitles_needed,
                'music': music_needed,
            }
            
            # 4. Simulate Processing
            with st.spinner('Applying edits, transitions, and brightness controls...'):
                processed_data, edit_summary = simulate_video_processing(uploaded_file, config)
                st.session_state.processing_done = True
                st.session_state.processed_data = processed_data
                st.session_state.edit_summary = edit_summary
                
            st.balloons()
            st.success("🎉 Processing Complete! Review the results below.")


# --- 5. RESULTS DISPLAY ---

if st.session_state.processing_done:
    st.markdown("## Processing Results", anchor="results")
    st.markdown("---")
    
    col_results1, col_results2 = st.columns(2)
    
    # Summary Result
    with col_results1:
        if st.session_state.summary:
            st.markdown(
                f"""
                <div class='result-box'>
                    <h3 style='color: #E0E0E0;'>Video Summary & Highlights</h3>
                    <p>{st.session_state.summary}</p>
                    <p style='font-size: 0.9em; font-weight: bold; color: #FF6B6B;'>Inferred Mood: {st.session_state.mood}</p>
                </div>
                """, unsafe_allow_html=True
            )

    # Music Recommendation Result
    with col_results2:
        if st.session_state.music_rec:
            st.markdown(
                f"""
                <div class='result-box music-box'>
                    <h3 style='color: #E0E0E0;'>Music Recommendation</h3>
                    <p>{st.session_state.music_rec}</p>
                    <pre style='background: #121212; padding: 10px; border-radius: 5px; color: #FFC300;'>{st.session_state.music_details}</pre>
                </div>
                """, unsafe_allow_html=True
            )

    st.markdown("### Edit Report and Download")
    st.markdown(
        f"""
        <div class='result-box' style='border-left: 5px solid #4ECDC4;'>
            <h4 style='color: #E0E0E0;'>AI Edits Applied:</h4>
            <ul style='list-style-type: none; padding-left: 0;'>
                {st.session_state.edit_summary.replace('- ', '<li><span style="color: #4ECDC4;">&#10003;</span> ')}
            </ul>
        </div>
        """, unsafe_allow_html=True
    )
    
    # --- Download Section ---
    st.markdown("#### Download Your Edited File")

    # Encode the simulated file data for download
    b64_data = base64.b64encode(st.session_state.processed_data).decode()
    new_filename = f"edited_{uploaded_file.name}"
    
    download_link = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{new_filename}" style="background-color: #4ECDC4; color: white; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; transition: background-color 0.2s;">Download Processed File ({new_filename})</a>'
    
    st.markdown(download_link, unsafe_allow_html=True)
    st.caption("*(Note: This is a simulated file download for demonstration purposes.)*")

else:
    st.info("Please upload a video or audio file to begin editing.")
    
# --- Footer Note ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 0.8em; color: #666666;'>
        *This application simulates complex video processing and AI tasks using Python's Streamlit framework and mock functions for core features like transition control and brightness adjustment based on the text prompt.*
    </div>
    """, unsafe_allow_html=True
)