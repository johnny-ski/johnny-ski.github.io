import os

# Paths
SOURCE_DIR = "songs-text"
OUTPUT_DIR = "."
SONGS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "songs-html")

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
      color: #0066cc;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .back-link {{
      display: inline-block;
      margin-bottom: 1rem;
      font-size: 20px;
    }}
    h1 {{
      font-size: 28px;
      margin-bottom: 1rem;
    }}
    img {{
      max-width: 100%;
      height: auto;
      border-radius: 12px;
      margin-bottom: 1rem;
    }}
  </style>
</head>
<body>
  <a class="back-link" href="../index.html">&larr; Back to Song List</a>
  <h1>{title}</h1>
  {image_html}
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
      font-family: monospace;
      background: #fdfdfd;
      max-width: 700px;
      margin: 2rem auto;
      padding: 1rem;
      line-height: 1.6;
      color: #333;
      font-size: 20px;
    }}
    h1 {{
      font-size: 28px;
      margin-bottom: 1rem;
    }}
    ul {{
      list-style-type: none;
      padding-left: 0;
    }}
    li {{
      margin-bottom: 0.5rem;
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
  <h1>Song List for NIST Friday Jam</h1>
  <ul>
    {links}
  </ul>
</body>
</html>
"""

def generate_site():
    os.makedirs(SONGS_OUTPUT_DIR, exist_ok=True)

    song_links = []

    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(SOURCE_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Remove trailing blank lines
            while lines and not lines[-1].strip():
                lines.pop()

            # Check for YouTube link at end
            youtube_url = ""
            if lines and lines[-1].strip().startswith(("https://www.youtube.com", "https://youtu.be")):
                youtube_url = lines[-1].strip()
                lines = lines[:-1]

            # First non-empty line = title
            title = ""
            content_start = 0
            for i, line in enumerate(lines):
                if line.strip():
                    title = line.strip()
                    content_start = i + 1
                    break

            # Robust IMAGE detection
            image_url = ""
            if content_start < len(lines):
                line = lines[content_start].strip()
                if line.upper().startswith("IMAGE:"):
                    image_url = line.split(":", 1)[1].strip()
                    content_start += 1

            # Collect lyrics (preserve spacing)
            lyrics_lines = lines[content_start:]
            lyrics = "".join(lyrics_lines).strip()

            # Append YouTube link inside lyrics
            if youtube_url:
                lyrics += f'\n\n🎵 <a href="{youtube_url}" target="_blank">Watch on YouTube</a>'

            # Build image HTML
            image_html = ""
            if image_url:
                image_html = f'<img src="../{image_url}">'

            # Generate HTML file
            output_filename = os.path.splitext(filename)[0] + ".html"
            output_path = os.path.join(SONGS_OUTPUT_DIR, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(PAGE_TEMPLATE.format(
                    title=title,
                    lyrics=lyrics,
                    image_html=image_html
                ))

            song_links.append((title, output_filename))

    # Sort alphabetically
    song_links.sort(key=lambda x: x[0])

    # Add hearts for Love Story
    links_html = "\n    ".join(
        f'<li><a href="songs-html/{filename}">{"❤️❤️❤️ " + title + " ❤️❤️❤️" if "Love Story" in title else title}</a></li>'
        for title, filename in song_links
    )

    # Write index.html
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX_TEMPLATE.format(links=links_html))

    print("Site generated in", OUTPUT_DIR)


if __name__ == "__main__":
    generate_site()
