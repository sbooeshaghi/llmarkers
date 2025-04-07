import sys
import unicodedata
from unidecode import unidecode
import re

def norm_text(text):
    if not isinstance(text, str):
        try:
            text = str(text)
        except:
            return ""

    text = unicodedata.normalize("NFC", text)
    text = unidecode(text)

    char_map = {
        "–": "-", "—": "--", "‘": "'", "’": "'", "“": '"', "”": '"', "…": "...",
        "•": "*", "·": ".", "×": "x", "÷": "/", "≤": "<=", "≥": ">=", "≠": "!=",
        "≈": "~", "∞": "inf", "∂": "d", "∫": "integral", "∑": "sum", "∏": "product",
        "√": "sqrt", "∝": "prop to", "∠": "angle", "△": "triangle", "□": "square",
        "∈": "in", "∉": "not in", "⊂": "subset", "⊃": "superset", "∪": "union",
        "∩": "intersect", "⊆": "subseteq", "⊇": "superseteq",
    }

    for char, replacement in char_map.items():
        text = text.replace(char, replacement)

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text

if __name__ == "__main__":
    for line in sys.stdin:
        normalized_line = norm_text(line)
        print(normalized_line)
