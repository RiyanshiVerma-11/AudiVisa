import pyttsx3
import tempfile
import os

def speak_text(text, rate=150, voice_name=None):
    """
    Convert text to speech and play it using pyttsx3.
    :param text: Text to be spoken.
    :param rate: Speech speed (default is 150).
    :param voice_name: Optional voice name or gender preference ('male', 'female').
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    # Set voice based on gender preference
    voices = engine.getProperty('voices')
    if voice_name == 'male':
        for voice in voices:
            if "male" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    elif voice_name == 'female':
        for voice in voices:
            if "female" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    engine.say(text)
    engine.runAndWait()

def save_tts_to_file(text, rate=150, voice_name=None):
    """
    Save the spoken text to an MP3 file using pyttsx3.
    :return: Path to the saved audio file.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    voices = engine.getProperty('voices')
    if voice_name == 'male':
        for voice in voices:
            if "male" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    elif voice_name == 'female':
        for voice in voices:
            if "female" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        file_path = fp.name
    engine.save_to_file(text, file_path)
    engine.runAndWait()
    return file_path
