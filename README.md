

# 🎓 Personalized Learning Assistant – Streamlit Web App

An AI-powered web application that enhances learning experiences by extracting subtitles from videos and generating downloadable `.srt` files. Built with Streamlit, OpenAI Whisper, and FFmpeg, this app makes video content more accessible and easier to follow.

---

## 🚀 Features

- 🎥 Upload educational or lecture videos
- 🔊 Convert video to audio using FFmpeg
- 🧠 Transcribe audio to text using OpenAI's Whisper
- 📝 Generate accurate, time-synced `.srt` subtitle files
- 📽️ Display subtitles live while video is playing
- 💾 Download subtitles as `.srt` files for external use

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:**
  - [Python](https://www.python.org/)
  - [OpenAI Whisper](https://github.com/openai/whisper) for transcription
  - [FFmpeg](https://ffmpeg.org/) + [Pydub](https://github.com/jiaaro/pydub) for audio processing
- **Utilities:** OS, datetime, tempfile, base64

---

## 📦 Installation

### 🔧 Prerequisites

- Python 3.8+
- FFmpeg installed and added to system path

### 📥 Clone the repository

```bash
git clone https://github.com/yourusername/personalized-learning-assistant.git
cd personalized-learning-assistant
````

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
streamlit run app.py
```

Then open the app in your browser at: [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure

```
personalized-learning-assistant/
├── app.py                  # Main Streamlit app
├── utils.py                # Utility functions (audio processing, SRT generation)
├── requirements.txt        # Python dependencies
├── test1.png               # Optional display image
└── README.md               # You're here!
```

---

## 📌 How It Works

1. **Upload Video** – User uploads a `.mp4` file
2. **Audio Extraction** – Video is converted to `.wav` using FFmpeg
3. **Transcription** – Whisper transcribes audio into text with timestamps
4. **SRT File Generation** – Converts timestamps to `.srt` format
5. **Live Subtitle Display** – Streamlit shows synchronized subtitles as video plays
6. **Download** – User can download subtitles for reuse

---

## 🧠 Future Enhancements

* 🔤 Multi-language transcription
* 🧑‍🏫 Speaker diarization (who spoke what)
* 📄 Summarized transcript generation
* ☁️ Deploy on Streamlit Cloud with public video link support

---

## 👨‍💻 Author

**Vignesh**
📬 [LinkedIn](https://www.linkedin.com/in/yourprofile)
💻 Passionate about AI, EdTech, and building impactful tools.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## ⭐️ Support

If you find this project useful, please consider giving it a ⭐️ on GitHub and sharing it!


Let me know if you want me to generate a `requirements.txt` file or add a license section. I can also generate a GitHub repository name suggestion.
