from deep_translator import GoogleTranslator

def translate_text(text, target_lang):
    """
    Translate the input text into the target language using deep-translator's GoogleTranslator.
    :param text: Input text to translate.
    :param target_lang: Target language code (e.g., 'hi' for Hindi).
    :return: Translated text or error message.
    """
    print(f"[DEBUG] Translating to '{target_lang}': {text}")  # Debug message

    if not text.strip():
        return "[Translation failed: Empty input]"

    try:
        translated = GoogleTranslator(target=target_lang).translate(text)
        print(f"[DEBUG] Translation result: {translated}")  # Debug output
        return translated
    except Exception as e:
        print(f"[ERROR] Translation failed: {e}")
        return f"[Translation failed: {str(e)}]"
