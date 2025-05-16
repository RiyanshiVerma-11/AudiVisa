# utils/stt.py

import speech_recognition as sr

def speech_to_text(timeout=5, phrase_time_limit=10):
    """
    Converts speech from the microphone into text using Google's Web Speech API.

    Args:
        timeout (int): Max time to wait for phrase to start (default: 5 seconds).
        phrase_time_limit (int): Max length of phrase in seconds (default: 10 seconds).

    Returns:
        str: Transcribed text or an error message.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening...")
        
        # Optional: adjust for ambient noise (improves accuracy in noisy environments)
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            # Capture the audio with timeout and phrase time limit
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return "⏱️ Listening timed out. Please try again."

    try:
        # Transcribe speech to text using Google's API
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "🤷 Could not understand audio."
    except sr.RequestError:
        return "🌐 Speech-to-text service unavailable."
