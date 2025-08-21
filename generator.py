import os

# Paths
SOURCE_DIR = "songs"
OUTPUT_DIR = "site"
SONGS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "songs")

# HTML templates
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{
      font-family: monospace;
      background: #fdfdfd;
      max-width: 700px;
      margin: 2rem auto;
      padding: 1rem;
      line-height: 1.6;
      color: #333;
    }}
    pre {{
      white-space: pre-wrap;
      background: #f9f9f9;
      padding: 1rem;
      border-radius: 8px;
      border: 1px solid #ddd;
      font-size: 20px;
    }}
    a {{
      display: inline-block;
      margin-bottom: 1rem;
      color: #0066cc;
      text-decoration: none;
    }}
    h1 {{
      font-size: 28px;
      margin-bottom: 1rem;
    }}
  </style>
</head>
<body>
  <a href="../index.html">&larr; Back to Song List</a>
  <h1>{title}</h1>
  <pre>{lyrics}</pre>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Song List</title>
  <style>
    body {{
      font-family: sans-serif;
      max-width: 700px;
      margin: 2rem auto;
      padding: 1rem;
      line-height: 1.8;
      font-size: 20px;
    }}
    h1 {{
      font-size: 28px;
    }}
    a {{
      color: #0066cc;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <h1>Song List</h1>
  <ul>
    {links}
  </ul>
</body>
</html>
"""

def generate_site():
    # Make output dirs
    os.makedirs(SONGS_OUTPUT_DIR, exist_ok=True)

    links = []

    for filename in sorted(os.listdir(SOURCE_DIR)):
        if filename.endswith(".txt"):
            filepath = os.path.join(SOURCE_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                lyrics = f.read()

            title = os.path.splitext(filename)[0].replace("_", " ").title()
            song_html = PAGE_TEMPLATE.format(title=title, lyrics=lyrics)

            output_filename = os.path.splitext(filename)[0] + ".html"
            output_path = os.path.join(SONGS_OUTPUT_DIR, output_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(song_html)

            links.append(f'<li><a href="songs/{output_filename}">{title}</a></li>')

    index_html = INDEX_TEMPLATE.format(links="\n    ".join(links))
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    print("Site generated in", OUTPUT_DIR)

if __name__ == "__main__":
    generate_site()
