import os

#count_files
docs_dir = "./raw_content"  # adjust if needed
markdown_files = []

for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith(".md"):
            markdown_files.append(os.path.join(root, file))


print(f"Found {len(markdown_files)} markdown files.")
print(markdown_files)

#read_files
for md_path in markdown_files:
    with open(md_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        print(raw_text)