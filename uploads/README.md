pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
<!-- virtual envirnment -->



to be installed//////////////////////////////////////

pip install pyttsx3
pip install streamlit pdfplumber
pip install gTTS pygame



# ------------------------------------------------------------
# 🧑‍💻 Developer Notes - AudiVisa Learning
# ------------------------------------------------------------


# Change the execution policy (permanent or for current user)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser


# ▶ Virtual Environment Setup (Windows)
 -------------------------------------
# 1. Create a new virtual environment
python -m venv venv

# 2. Activate the virtual environment
venv\Scripts\activate

# 3. Install all required packages
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run app.py





streamlit==1.32.2
pdfplumber==0.10.3
pytesseract==0.3.10
Pillow==10.2.0
speechrecognition==3.10.1
gtts==2.5.1
transformers==4.40.0
torch>=2.0.0
sentencepiece==0.2.0
googletrans==4.0.0rc1
pydub==0.25.1




i am using til now 
streamlit
pdfplumber
pytesseract
Pillow
gTTS
pygame
pyttsx3
SpeechRecognition
googletrans==4.0.0rc1
transformers
torch





i have intalled thsi too...........
pip install pipwin
pipwin install pyaudio






if "splash_shown" not in st.session_state:
    import base64
    from io import BytesIO

    def get_base64_image(image_path):
        img = Image.open(image_path)
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode()

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

    # Set flag in session state to prevent rerun
    st.session_state.splash_shown = True
    time.sleep(6)
    st.rerun()  # This will only rerun once after the splash screen
