# 🇮🇳 Mana-Corpus: Offline Indic Corpus Collector

**Mana-Corpus (మన-కార్పస్)** is an open-source, AI-powered Streamlit application built for **offline Indic corpus collection**. It enables individuals and researchers to contribute text, audio, image, and video content across 22+ Indian languages—completely without the internet.

This app supports **geo-tagged and categorized data collection**, making it ideal for preserving rich cultural datasets from rural and remote regions.

---

## ✨ Features

- 🎙️ **Multimodal Data Collection** – Collect **Text**, **Audio**, **Image**, and **Video**
- 🌐 **Offline-First Design** – Works entirely offline, perfect for rural deployments
- 📍 **Geo Coordinates Capture** – Latitude/Longitude captured per entry
- 👤 **User Details Input** – Collect contributor metadata (Name, Age, Location)
- 🏷️ **Corpus Categorization** – Choose from categories like:
  - Childhood Games
  - Handcraft Skills
  - Folk Songs & Stories
  - Traditional Farming
  - Local Rituals and some more
- 📝 **Title + Description Fields** – For every entry across all media types
- 🔤 **Indic Language Detection** – Auto-identifies input language
- 📦 **Data Backup Support** – Export collected data as ZIP file for USB transfer

---

## 📁 Project Structure

```
Mana-Corpus/
│
├── app.py                     # Main Streamlit App
├── requirements.txt           # Dependencies
├── README.md                  # Project Documentation
│
├── data/                      # Offline Collected Data
│   ├── audio/
│   ├── images/
│   ├── videos/
│   └── text_corpus.txt
│
├── utils/                     # Helper Modules
│   ├── audio_utils.py
│   ├── image_utils.py
│   └── nlp_utils.py
│
├── sync/                      # ZIP backup module
│   └── sync_utils.py
│
└── models/                    # (Optional) AI/NLP Models
```

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.9+
- Streamlit 1.30+
- Works Offline!

### 📦 Installation

```bash
# 1. Clone the Repo
git clone https://code.swecha.org/soai2025/soai-hackathon/Mana-corpus.git
cd Mana-corpus

# 2. Setup Virtual Environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run the App
streamlit run app.py
```

---

## 🌍 How It Works

1. Launch the app using `streamlit run app.py`
2. Choose a **Corpus Category** (e.g., Handcraft Skills)
3. Enter:
   - 🧑 User details
   - 📍 Geo Coordinates (auto/manual)
   - 🏷️ Title & Description
4. Upload **Text**, **Image**, **Audio**, or **Video**
5. Click ✅ `Save Data` to store offline in `/data/`
6. Use **Backup** tab to generate a `.zip` for USB transfer.

---

## 🛡️ Data Privacy

This app works **entirely offline**. No personal or data entries are uploaded to the internet unless you choose to back up and share the files yourself.

---

## 🤝 Contributors

- Akshay Kumar Y  
- Nagaraj CH  
- Bhuvaneswar  
- Sai Sashindra K  
- Srujit Kumar  

Made with ❤️ at **IIIT Hyderabad Hackathon 2025**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌐 Future Plans

- 🗣️ Offline Speech-to-Text for Audio
- 📲 Android APK using Streamlit + PWA
- 🔤 Indic OCR for Image Text Extraction
- 📊 Corpus Dashboard & Stats
