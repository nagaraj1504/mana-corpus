import streamlit as st
import os
import json
import geocoder
from datetime import datetime
import random
import string
from utils.nlp_utils import clean_text, detect_language
from utils.image_utils import is_image_file, get_image_info
from utils.audio_utils import is_audio_file, get_audio_duration
from sync.sync_utils import create_backup_zip


def send_otp(phone_number):
    otp = ''.join(random.choices(string.digits, k=6))
    st.session_state.otp = otp
    st.session_state.otp_timestamp = datetime.now()
    return otp


def verify_otp(entered_otp):
    if 'otp' not in st.session_state:
        return False, "No OTP sent yet"

    if datetime.now() - st.session_state.otp_timestamp > datetime.timedelta(minutes=5):
        return False, "OTP expired"

    if entered_otp == st.session_state.otp:
        return True, "OTP verified successfully"
    return False, "Invalid OTP"


def get_geo_location():
    g = geocoder.ip('me')
    if g.ok:
        lat, lon = g.latlng
        return str(lat), str(lon)
    return "17.3850", "78.4867"


def collect_metadata():
    user_name = st.text_input("👤 Contributor's Name:")
    user_location = st.text_input("📍 Location (Village / Town / City):")
    auto_lat, auto_lon = get_geo_location()
    st.markdown("### 📍 Location (Auto-Detect + Manual Entry)")
    st.info(f"🌐 Auto-Detected (or Default) Location: **{auto_lat}, {auto_lon}**")
    manual_lat = st.text_input("Latitude (you can override)", value=auto_lat)
    manual_lon = st.text_input("Longitude (you can override)", value=auto_lon)
    title = st.text_input("📝 Title of the Entry:")
    description = st.text_area("🖊️ Short Description (Context / Details):")
    return {
        "contributor": user_name,
        "location": user_location,
        "latitude": manual_lat,
        "longitude": manual_lon,
        "category": st.session_state.category,
        "title": title,
        "description": description,
        "timestamp": datetime.now().isoformat()
    }


def go_home():
    st.session_state.page = "home"
    st.session_state.category = None


# Page Config
st.set_page_config(page_title="Mana-Corpus", layout="wide")
st.title("🇮🇳 Mana-Corpus: Offline Indic Corpus Collection")

# Session State Initialization
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'category' not in st.session_state:
    st.session_state.category = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'location': '',
        'latitude': '',
        'longitude': '',
        'total_contributions': 0,
        'text_contribs': 0,
        'audio_contribs': 0,
        'image_contribs': 0,
        'video_contribs': 0,
        'last_contribution': None
    }
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'auth_method' not in st.session_state:
    st.session_state.auth_method = None
if 'otp' not in st.session_state:
    st.session_state.otp = None
if 'otp_timestamp' not in st.session_state:
    st.session_state.otp_timestamp = None

# Top right login/profile
if st.session_state.is_authenticated:
    if st.button("👤 Profile", key="profile_btn"):
        st.session_state.page = "profile"
else:
    if st.button("🔒 Login", key="login_btn_top"):
        st.session_state.page = "login"

# ---------------- PROFILE ----------------
if st.session_state.page == "profile":
    st.header("👤 User Profile")

    with st.expander("Current Profile Information", expanded=True):
        profile = st.session_state.user_profile
        st.write(f"**Name:** {profile['name']}")
        st.write(f"**Location:** {profile['location']}")
        st.write(f"**Coordinates:** {profile['latitude']}, {profile['longitude']}")

        st.markdown("### 📊 Your Contributions")
        left_col, right_col = st.columns(2)
        with left_col:
            st.metric("📝 Total Contributions", f"{profile['total_contributions']:,}")
            st.metric("📄 Text Contributions", f"{profile['text_contribs']:,}")
        with right_col:
            st.metric("🎤 Audio Contributions", f"{profile['audio_contribs']:,}")
            st.metric("📸 Image Contributions", f"{profile['image_contribs']:,}")
            st.metric("🎥 Video Contributions", f"{profile['video_contribs']:,}")

    with st.form("edit_profile", clear_on_submit=True):
        st.markdown("### 📝 Edit Profile")
        name = st.text_input("👤 Your Name", value=profile['name'])
        location = st.text_input("📍 Location", value=profile['location'])
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.text_input("Latitude", value=profile['latitude'])
        with col2:
            longitude = st.text_input("Longitude", value=profile['longitude'])
        if st.form_submit_button("Update Profile"):
            profile.update({
                'name': name,
                'location': location,
                'latitude': latitude,
                'longitude': longitude
            })
            st.success("Profile updated successfully!")

    if st.button("⬅️ Back to Home"):
        go_home()

# ---------------- LOGIN ----------------
if st.session_state.page == "login":
    st.title("🔒 Login")
    tab1, tab2 = st.tabs(["📱 OTP Login", "📱 Password Login"])

    with tab1:
        st.header("📱 Login with OTP")
        with st.form("otp_login", clear_on_submit=True):
            phone_number = st.text_input("📱 Phone Number")
            if st.form_submit_button("Send OTP"):
                if phone_number:
                    st.session_state.otp = send_otp(phone_number)
                    st.success("OTP sent successfully! Please check your phone.")
                else:
                    st.error("Please enter your phone number")

    with tab2:
        st.header("📱 Login with Password")
        with st.form("password_login", clear_on_submit=True):
            phone_number = st.text_input("📱 Phone Number")
            password = st.text_input("🔑 Password", type="password")
            if st.form_submit_button("Login"):
                if len(phone_number) != 10 or not phone_number.isdigit():
                    st.error("Please enter a valid 10-digit mobile number")
                elif not password:
                    st.error("Please enter your password")
                else:
                    st.success("Login successful!")
                    st.session_state.is_authenticated = True
                    st.session_state.page = "home"

    if st.button("📝 Register", key="register_btn"):
        st.session_state.page = "register"

# ---------------- HOME WITH TABS ----------------
if st.session_state.page == "home" and st.session_state.is_authenticated:
    st.header("🏠 Home - Select Corpus Category")

    categories = [
        "Agriculture", "Health", "Childhood Games", "Traditional Knowledge",
        "Small Business", "Education", "Law", "Home & Lifestyle", "Others"
    ]

    tabs = st.tabs([f"📂 {cat}" for cat in categories])

    for i, tab in enumerate(tabs):
        with tab:
            cat = categories[i]
            st.session_state.category = cat
            st.markdown(f"### 🗂️ {cat} - Select Corpus Type")
            if st.button("📄 Text Corpus", key=f"text_{cat}"):
                st.session_state.page = "text"
            if st.button("🎤 Audio Corpus", key=f"audio_{cat}"):
                st.session_state.page = "audio"
            if st.button("📸 Image Corpus", key=f"image_{cat}"):
                st.session_state.page = "image"
            if st.button("🎥 Video Corpus", key=f"video_{cat}"):
                st.session_state.page = "video"

# ---------------- TEXT ----------------
if st.session_state.page == "text":
    st.header(f"📄 {st.session_state.category} - Text Corpus")
    metadata = collect_metadata()
    user_text = st.text_area("💬 Corpus Text:")
    if st.button("Submit Text Corpus"):
        cleaned_text = clean_text(user_text)
        lang = detect_language(cleaned_text)
        if cleaned_text.strip():
            metadata.update({"text": cleaned_text, "language_detected": lang})
            save_path = os.path.join("data/text", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            st.success("✅ Text Corpus saved successfully.")
            go_home()
        else:
            st.warning("⚠️ Please provide valid text.")
    if st.button("⬅️ Back to Home"):
        go_home()

# ---------------- AUDIO ----------------
if st.session_state.page == "audio":
    st.header(f"🎤 {st.session_state.category} - Audio Corpus")
    metadata = collect_metadata()
    uploaded_files = st.file_uploader("Upload Audio Files", accept_multiple_files=True, type=["wav", "mp3", "ogg", "flac"])
    if uploaded_files and st.button("Submit Audio Files"):
        os.makedirs("data/audio", exist_ok=True)
        for file in uploaded_files:
            if is_audio_file(file.name):
                file_path = os.path.join("data/audio", file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                duration = get_audio_duration(file_path)
                metadata.update({"audio_file": file.name, "duration_seconds": duration})
                save_json = os.path.join("data/audio", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(save_json, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=4)
                st.success(f"✅ Saved {file.name} with metadata.")
        go_home()
    if st.button("⬅️ Back to Home"):
        go_home()

# ---------------- IMAGE ----------------
if st.session_state.page == "image":
    st.header(f"📸 {st.session_state.category} - Image Corpus")
    metadata = collect_metadata()
    uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    if uploaded_files and st.button("Submit Image Files"):
        os.makedirs("data/images", exist_ok=True)
        for file in uploaded_files:
            if is_image_file(file.name):
                file_path = os.path.join("data/images", file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                info = get_image_info(file_path)
                metadata.update({"image_file": file.name, "image_info": info})
                save_json = os.path.join("data/images", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(save_json, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=4)
                st.success(f"✅ Saved {file.name} with metadata.")
        go_home()
    if st.button("⬅️ Back to Home"):
        go_home()

# ---------------- VIDEO ----------------
if st.session_state.page == "video":
    st.header(f"🎥 {st.session_state.category} - Video Corpus")
    metadata = collect_metadata()
    uploaded_files = st.file_uploader("Upload Videos", accept_multiple_files=True, type=["mp4", "mkv"])
    if uploaded_files and st.button("Submit Video Files"):
        os.makedirs("data/videos", exist_ok=True)
        for file in uploaded_files:
            file_path = os.path.join("data/videos", file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            metadata.update({"video_file": file.name})
            save_json = os.path.join("data/videos", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(save_json, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            st.success(f"✅ Saved {file.name} with metadata.")
        go_home()
    if st.button("⬅️ Back to Home"):
        go_home()

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("© 2025 Mana-Corpus • AI-Powered Indic Corpus Collection")
