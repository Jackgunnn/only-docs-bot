import os

# Directory to search for markdown files
docs_dir = "./raw_content"
markdown_files = []

# Collect all .md file paths
for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith(".md"):
            markdown_files.append(os.path.join(root, file))

# Write all contents into one file
with open("all_raw_text.txt", "w", encoding="utf-8") as out:
    for md_path in markdown_files:
        with open(md_path, "r", encoding="utf-8") as f:
            out.write(f"## FILE: {md_path}\n\n")
            out.write(f.read() + "\n\n")

print(f"✅ Saved {len(markdown_files)} markdown files to all_raw_text.txt")
