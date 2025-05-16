# utils/braille_converter.py

# ✅ Braille mappings for alphabets a–z
braille_dict = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵'
}

# ✅ Braille mappings for numbers 0–9 using number sign prefix ⠼
braille_digits = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚'
}

def convert_to_braille(text):
    """
    Convert a string to Braille Unicode.
    Supports a-z and 0–9, with number sign prefix for digits.
    Other characters (punctuation/whitespace) are preserved.
    """
    braille_output = ""
    for char in text.lower():
        if char.isalpha():
            braille_output += braille_dict.get(char, char)
        elif char.isdigit():
            braille_output += "⠼" + braille_digits.get(char, char)
        else:
            braille_output += char  # Keep punctuation, symbols, etc.
    return braille_output
