# utils/braille.py

# 🔡 Braille Unicode mappings for alphabets a–z
braille_alphabet = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
    "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
    "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
    "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵"
}

# 🔢 Digits in Braille use a-j with a leading number sign ⠼
braille_digits = {
    "1": "⠁", "2": "⠃", "3": "⠉", "4": "⠙", "5": "⠑",
    "6": "⠋", "7": "⠛", "8": "⠓", "9": "⠊", "0": "⠚"
}

def convert_to_braille(text):
    """
    Converts input text (letters and digits) into Braille.
    - Letters are mapped to Braille letters.
    - Digits are prefixed with ⠼ and mapped to a–j Braille.
    - Spaces are preserved.
    - Punctuation is ignored for now (can be extended later).
    """
    output = ""
    for char in text:
        if char.isalpha():
            output += braille_alphabet.get(char.lower(), "")
        elif char.isdigit():
            output += "⠼" + braille_digits[char]
        elif char == " ":
            output += " "
        else:
            # Punctuation and other symbols are ignored.
            output += ""
    return output
