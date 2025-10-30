import re
from bs4 import BeautifulSoup

def clean_text(text):
    # 1️⃣ Remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()

    # 2️⃣ Remove YAML front matter
    text = re.sub(r"^---[\s\S]*?---\s*", "", text, flags=re.MULTILINE)

    # 3️⃣ Extract and temporarily replace code blocks
    code_blocks = {}
    def save_code_block(match):
        key = f"@@CODE{len(code_blocks)}@@"
        code_blocks[key] = match.group(0)
        return key
    text = re.sub(r"```[\s\S]*?```|`[^`]+`", save_code_block, text)

    # 4️⃣ Remove markdown formatting symbols
    text = re.sub(r"[#*_>\[\]{}~=]+", " ", text)

    # 5️⃣ Remove markdown list bullets
    text = re.sub(r"(?m)^\s*(?:[-*]|\d+[.)])\s+", "", text)

    # 6️⃣ Keep only readable chars (letters, digits, punctuation, links)
    text = re.sub(r"[^A-Za-z0-9:/._\-\s\n!?]", " ", text)

    # 7️⃣ Normalize all existing line breaks to spaces
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"[ \t]+", " ", text).strip()

    # 8️⃣ Split sentences → remove punctuation → newline
    text = re.sub(r'[.!?]\s+(?=[A-Z0-9])', r'\n', text)

    # 9️⃣ Restore code blocks
    for key, value in code_blocks.items():
        text = text.replace(key, value)

    return text


# --- Read raw file ---
with open("data/all_raw_text.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# --- Clean and split sentences ---
cleaned = clean_text(raw)

# --- Save to a new text file ---
with open("data/cleaned_sentences.txt", "w", encoding="utf-8") as f:
    f.write(cleaned)

print("✅ Sentence-per-line text saved to cleaned_sentences.txt")
