import os
import re
from bs4 import BeautifulSoup

def load_data(docs_dir="raw_content", output_file="data/raw_data.txt"):
    """
    Loads all markdown (.md) files from a directory and
    combines their content into a single text file.

    Args:
        docs_dir (str): Directory to search for markdown files.
        output_file (str): Path to save the combined text.
    """

    markdown_files = []

    # Collect all .md file paths
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))

    # Write all contents into one file
    i = 1
    with open(output_file, "w", encoding="utf-8") as out:
        for md_path in markdown_files:
            print(i, md_path)
            with open(md_path, "r", encoding="utf-8") as f:
                file_content = f.read()
                out.write(f"## FILE: {md_path}\n\n{file_content}\n\n")
            i+=1

    print(f"Saved {len(markdown_files)} markdown files to {output_file}")


def clean_data(input_file="data/raw_data.txt", output_file="data/cleaned_data.txt"):
    """
    Cleans the raw data file and saves the cleaned data 
    into a single text file.

    Args:
        input_file (str): Directory to search for markdown files.
        output_file (str): Path to save the combined text.  
    """

    # --- Read raw file ---
    with open(input_file, "r", encoding="utf-8") as f:
        raw = f.read()

    # Remove HTML tags
    soup = BeautifulSoup(raw, "html.parser")
    raw = soup.get_text()

    # Remove YAML front matter
    raw = re.sub(r"^---[\s\S]*?---\s*", "", raw, flags=re.MULTILINE)

    # Remove markdown formatting symbols
    raw = re.sub(r"[#*_>\[\]{}~=]+", " ", raw)

    # Remove markdown list bullets
    raw = re.sub(r"(?m)^\s*(?:[-*]|\d+[.)])\s+", "", raw)

    # Keep only readable chars (letters, digits, punctuation, links)
    raw = re.sub(r"[^A-Za-z0-9:/._\-\s\n!?]", " ", raw)

    # Normalize all existing line breaks to spaces
    raw = re.sub(r"\n+", " ", raw)
    raw = re.sub(r"[ \t]+", " ", raw).strip()

    # Split sentences → remove punctuation → newline
    raw = re.sub(r'[.!?]\s+(?=[A-Z0-9])', r'\n', raw)

    # --- Save to a new text file ---
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(raw)

    print(f"Cleaned Data saved to {output_file}")

load_data()
clean_data()