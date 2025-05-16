import streamlit as st
from PIL import Image
import time
import base64
from io import BytesIO
import asyncio
import os
import tempfile
from moviepy.editor import VideoFileClip
# from pytube import YouTube  # Removed unused import
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import yt_dlp



# Internal module imports
from utils.ocr_reader import extract_text_from_image
from pydub import AudioSegment
from utils.tts import speak_text, save_tts_to_file
from utils.stt import speech_to_text
from utils.translator import translate_text
from utils.summarizer import summarize_text
from utils.image_captioner import generate_image_caption
from utils.braille import convert_to_braille

# Fix for async event loop issue on Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_base64_image(image_path):
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    img_bytes = buffer.getvalue()
    return base64.b64encode(img_bytes).decode()

if "splash_shown" not in st.session_state:
    encoded_image = get_base64_image("front_page.jpg")
    st.markdown(f"""
        <style>
        .splash {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #ffffff;
            z-index: 10000;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            animation: fadeOut 1s ease-in-out 5s forwards;
        }}
        .splash img {{
            width: 60%;
            max-width: 600px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }}
        .splash-text {{
            margin-top: 20px;
            font-size: 1.6em;
            font-weight: bold;
            color: #333;
        }}
        @keyframes fadeOut {{
            to {{
                opacity: 0;
                visibility: hidden;
            }}
        }}
        </style>
        <div class="splash">
            <img src="data:image/jpeg;base64,{encoded_image}" />
            <div class="splash-text">Loading AudiVisa Learning...</div>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.splash_shown = True
    time.sleep(6)
    st.rerun()

st.set_page_config(page_title="AudiVisa Learning", layout="centered")
st.markdown("### 🎓 Inclusive Learning Platform")
st.markdown("Helping visually and hearing impaired students with accessible learning")

st.sidebar.header("📥 Choose Input Type")
option = st.sidebar.selectbox("Select input type", ["PDF", "Image", "Speech", "Text", "Video", "YouTube Video"])

# Add learner type selection here
learner_types = ["Visually Impaired", "Hearing Impaired", "Slow Learner", "Fast Learner"]
learner_type = st.sidebar.selectbox("Select Learner Type", learner_types)
st.session_state["learner_type"] = learner_type



languages = {
    "Assamese (অসমীয়া)": "as", "Bengali (বাংলা)": "bn", "Bodo (बोड़ो)": "hi",
    "Dogri (डोगरी)": "hi", "Gujarati (ગુજરાતી)": "gu", "Hindi (हिन्दी)": "hi",
    "Kannada (ಕನ್ನಡ)": "kn", "Kashmiri (کٲشُر)": "ur", "Konkani (कोंकणी)": "hi",
    "Maithili (मैथिली)": "hi", "Malayalam (മലയാളം)": "ml", "Manipuri (মৈতৈলোন্)": "bn",
    "Marathi (मराठी)": "mr", "Nepali (नेपाली)": "ne", "Odia (ଓଡ଼ିଆ)": "or",
    "Punjabi (ਪੰਜਾਬੀ)": "pa", "Sanskrit (संस्कृतम्)": "hi", "Santali (ᱥᱟᱱᱛᱟᱲᱤ)": "hi",
    "Sindhi (سنڌي‎)": "sd", "Tamil (தமிழ்)": "ta", "Telugu (తెలుగు)": "te",
    "Urdu (اُردُو)": "ur", "English": "en"
}

def translation_ui(text):
    if not text:
        st.warning("No text to translate.")
        return
    lang_choice = st.selectbox("🌐 Translate to", list(languages.keys()))
    target_lang = languages[lang_choice]
    if st.button("🌍 Translate Text", key="translate_button"):
        translated = translate_text(text, target_lang)
        st.session_state["translated_text"] = translated
        st.session_state["tts_lang"] = target_lang  # Store the language code for TTS
    rate, voice = voice_controls(prefix="translate")
    if "translated_text" in st.session_state:
        translated = st.session_state["translated_text"]
        tts_lang = st.session_state.get("tts_lang", "en")  # Default to English if not set
        st.text_area("Translated Text", value=translated, height=200)
        if st.button("🔊 Read Translated Aloud", key="read_translated"):
            speak_text(translated, rate=rate, voice_name=voice, lang=tts_lang)  # Pass lang
        audio_path = save_tts_to_file(translated, rate=rate, voice_name=voice, lang=tts_lang)  # Pass lang
        if audio_path:
            with open(audio_path, "rb") as audio_file:
                st.download_button("💾 Download Translated Audio", data=audio_file, file_name="translated_output.mp3", mime="audio/mpeg")
    if st.button("🧠 Summarize Text", key="summarize_button"):
        summary = summarize_text(text)
        st.session_state["summary_text"] = summary
    if "summary_text" in st.session_state:
        st.text_area("Summary", value=st.session_state["summary_text"], height=150)

@st.cache_data
def cached_read_pdf(file):
    import pdfplumber
    with pdfplumber.open(file) as pdf:
        return "".join(page.extract_text() or "" for page in pdf.pages)
    
def transcribe_audio_in_chunks(wav_path, chunk_length_ms=60*1000):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(wav_path)
    duration_ms = len(audio)
    texts = []
    temp_dir = tempfile.mkdtemp()
    for i in range(0, duration_ms, chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunk_path = os.path.join(temp_dir, f"chunk_{i//chunk_length_ms}.wav")
        chunk.export(chunk_path, format="wav")
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except Exception as e:
            text = f"[Chunk {i//chunk_length_ms+1} transcription failed: {e}]"
        texts.append(text)
        os.remove(chunk_path)
    os.rmdir(temp_dir)
    return "\n".join(texts) 

def download_youtube_audio_with_ytdlp(youtube_url, output_dir):
    import yt_dlp
    import os

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, "audio.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    # After download, find the mp3 file
    mp3_path = os.path.join(output_dir, "audio.mp3")
    return mp3_path

def download_youtube_audio_and_transcribe(youtube_url, chunk_length_ms=60*1000):
    temp_dir = tempfile.mkdtemp()
    audio_path = download_youtube_audio_with_ytdlp(youtube_url, temp_dir)
    wav_path = os.path.splitext(audio_path)[0] + ".wav"
    AudioSegment.from_file(audio_path).export(wav_path, format="wav")
     # Transcribe the audio in chunks
    text = transcribe_audio_in_chunks(wav_path, chunk_length_ms=chunk_length_ms)
    # Clean up temp files
    try:
        os.remove(audio_path)
        os.remove(wav_path)
        os.rmdir(temp_dir)
    except Exception:
        pass
    return text



def voice_controls(prefix="default"):
    with st.expander("🎚 Speech Options"):
        rate = st.slider("Speech Speed", 50, 300, 150, 10, key=f"{prefix}_rate")
        voices = {"Default (System)": None, "Male": "male", "Female": "female"}
        voice_choice = st.selectbox("Voice Type", list(voices.keys()), key=f"{prefix}_voice")
    return rate, voices[voice_choice]

def translation_ui(text):
    if not text:
        st.warning("No text to translate.")
        return
    lang_choice = st.selectbox("🌐 Translate to", list(languages.keys()))
    target_lang = languages[lang_choice]
    if st.button("🌍 Translate Text", key="translate_button"):
        translated = translate_text(text, target_lang)
        st.session_state["translated_text"] = translated
    rate, voice = voice_controls(prefix="translate")
    if "translated_text" in st.session_state:
        translated = st.session_state["translated_text"]
        st.text_area("Translated Text", value=translated, height=200)
        if st.button("🔊 Read Translated Aloud", key="read_translated"):
            speak_text(translated, rate=rate, voice_name=voice)
        audio_path = save_tts_to_file(translated, rate=rate, voice_name=voice)
        if audio_path:
            with open(audio_path, "rb") as audio_file:
                st.download_button("💾 Download Translated Audio", data=audio_file, file_name="translated_output.mp3", mime="audio/mpeg")
    if st.button("🧠 Summarize Text", key="summarize_button"):
        summary = summarize_text(text)
        st.session_state["summary_text"] = summary
    if "summary_text" in st.session_state:
        st.text_area("Summary", value=st.session_state["summary_text"], height=150)

def braille_ui(text):
    if text:
        braille = convert_to_braille(text)
        with st.expander("🧑‍🦯 Braille Representation (A-Z, a-z)"):
            st.code(braille)

def handle_text_output(text):
    st.markdown("### 📄 Extracted Text")
    st.text_area("Text Output", value=text, height=200)
    rate, voice = voice_controls(prefix="output")
    if text and st.button("🔊 Read Aloud"):
        speak_text(text, rate=rate, voice_name=voice)
    braille_ui(text)


def extract_text_from_image(image, lang="eng"):
    # Example using pytesseract
    import pytesseract
    from PIL import Image

    # If 'image' is a file-like object, open it with PIL
    if not isinstance(image, Image.Image):
        image = Image.open(image)

    text = pytesseract.image_to_string(image, lang=lang)
    return text     


def show_quiz(text):
    st.subheader("📝 Quick Quiz")
    # Dummy question from content
    question = f"What is the main idea of the above content?"
    options = ["Option A", "Option B", "Option C", "Option D"]
    answer = st.radio(question, options)
    if st.button("Submit Answer"):
        if answer == "Option A":  # Replace with correct answer logic
            st.success("Correct!")
        else:
            st.error("Oops! Try reviewing the content again.")


if option == "PDF":
    uploaded_file = st.file_uploader("📄 Upload a PDF file", type=["pdf"])
    if uploaded_file:
        text = cached_read_pdf(uploaded_file)
        handle_text_output(text)
        translation_ui(text)

elif option == "Image":
    uploaded_img = st.file_uploader("🖼 Upload Image", type=["png", "jpg", "jpeg"])
    if uploaded_img:
        caption = generate_image_caption(uploaded_img)
        st.text_area("Generated Description", value=caption, height=100)
        rate, voice = voice_controls(prefix="caption")
        speak_text(caption, rate=rate, voice_name=voice)
        ocr_lang_choice = st.selectbox("Select OCR Language(s)", list(languages.keys()), key="ocr_lang")
        ocr_lang_code = languages[ocr_lang_choice]
        text = extract_text_from_image(uploaded_img, lang=ocr_lang_code)
        handle_text_output(text)
        translation_ui(text)

elif option == "Speech":
    st.write("🎙 Record speech or upload an audio file to convert to text")
    audio_file = st.file_uploader("Upload audio file (WAV/MP3)", type=["wav", "mp3"])
    if audio_file is not None:
        with st.spinner("Transcribing uploaded audio..."):
            # Save uploaded file to a temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix="." + audio_file.name.split('.')[-1]) as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            # Convert to wav if needed
            wav_path = tmp_path
            if not tmp_path.endswith(".wav"):
                wav_path = tmp_path.rsplit(".", 1)[0] + ".wav"
                AudioSegment.from_file(tmp_path).export(wav_path, format="wav")
            output = transcribe_audio_in_chunks(wav_path)
            st.success("✅ Transcription complete")
            handle_text_output(output)
            translation_ui(output)
            if "learner_type" in st.session_state:
                learner_type = st.session_state["learner_type"]
                if learner_type == "Visually Impaired":
                    st.markdown("Optimized for audio learning...")
                    speak_text(output)
                elif learner_type == "Hearing Impaired":
                    st.markdown("Visual explanation and Braille included...")
                    braille_ui(output)
    

elif option == "Text":
    user_input = st.text_area("✍ Enter your text")
    if user_input:
        handle_text_output(user_input)
        translation_ui(user_input)




elif option == "Video":
    st.subheader("🎥 Upload a Video File")
    video_file = st.file_uploader("Upload video (MP4 format)", type=["mp4"])
    if video_file:
        with st.spinner("🔊 Extracting and transcribing audio..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(video_file.read())
                tmp_path = tmp.name
            wav_path = tmp_path.replace(".mp4", ".wav")
            VideoFileClip(tmp_path).audio.write_audiofile(wav_path)
            text = transcribe_audio_in_chunks(wav_path)
        st.success("✅ Transcription complete")
        handle_text_output(text)
        translation_ui(text)

elif option == "YouTube Video":
    st.subheader("▶ Enter YouTube Video URL")
    youtube_url = st.text_input("Paste the YouTube video URL here")
    if youtube_url:
        if st.button("Transcribe YouTube Video"):
            with st.spinner("🔄 Downloading and transcribing..."):
                try:
                    text = download_youtube_audio_and_transcribe(youtube_url)
                    st.success("✅ Transcription complete")
                    handle_text_output(text)
                    translation_ui(text)
                    # Add here (after line 311)
                    if "learner_type" in st.session_state:
                       learner_type = st.session_state["learner_type"]
                       if learner_type == "Visually Impaired":
                           st.markdown("Optimized for audio learning...")
                           speak_text(text)
                       elif learner_type == "Hearing Impaired":
                           st.markdown("Visual explanation and Braille included...")
                           braille_ui(text)
                except Exception as e:
                    st.error(f"Failed to process YouTube video: {e}")