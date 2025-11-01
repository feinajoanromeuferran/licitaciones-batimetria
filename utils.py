import re
from dateutil import parser

KEYWORDS = [
    "batimetr", "batimetría", "batimetria",
    "topograf", "topografía", "topografia",
    "fondo marino", "fondo-marino",
    "levantamiento", "levantament",
    "aixecament", "topogràfic", "topografic"
]

def match_keywords(text):
    if not text:
        return False
    text_low = text.lower()
    return any(k in text_low for k in KEYWORDS)

def parse_date(s):
    try:
        return parser.parse(s, dayfirst=True)
    except Exception:
        return None