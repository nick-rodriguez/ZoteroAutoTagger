import re
import unicodedata

from bs4 import BeautifulSoup


def clean_text(text):
    if not text:
        return ""
    soup = BeautifulSoup(text, "html.parser")
    plain_text = soup.get_text(separator=" ").replace("\n", " ").strip()
    plain_text = re.sub(r'^\s*abstract\s+', '', plain_text, flags=re.IGNORECASE)
    return unicodedata.normalize("NFKD", plain_text)
