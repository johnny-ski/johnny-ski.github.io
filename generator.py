import os

# Paths
SOURCE_DIR = "songs-text"              # folder with your .txt files
OUTPUT_DIR = "."                        # root of repo for GitHub Pages
SONGS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "songs-html")  # folder for generated HTML

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
  </style>
</head>
<body>
  <a class="back-link" href="../index.html">&larr; Back to Song List</a>
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

  <!-- <img src="images/AJ.png" style="max-width:100%; height:auto; border-radius:12px;"> -->

</body>
</html>
"""

def generate_site():
    # Make output dirs
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

            # Check if last non-empty line is a YouTube link
            youtube_url = ""
            if lines and lines[-1].strip().startswith(("https://www.youtube.com", "https://youtu.be")):
                youtube_url = lines[-1].strip()
                lines = lines[:-1]  # remove it from lyrics

            # First non-empty line = title
            title = ""
            content_start = 0
            for i, line in enumerate(lines):
                if line.strip():
                    title = line.strip()
                    content_start = i + 1
                    break

            # Collect lyrics
            # lyrics_lines = [line for line in lines[content_start:] if line.strip() or line == "\n"]
            lyrics_lines = lines[content_start:]
            lyrics = "".join(lyrics_lines).strip()



            

            # If YouTube link present, append as pretty link inside lyrics
            if youtube_url:
                lyrics += f'\n\n🎵 <a href="{youtube_url}" target="_blank">Watch on YouTube</a>'

            # Generate HTML file
            output_filename = os.path.splitext(filename)[0] + ".html"
            output_path = os.path.join(SONGS_OUTPUT_DIR, output_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(PAGE_TEMPLATE.format(title=title, lyrics=lyrics))

            # Save title and file for sorting
            song_links.append((title, output_filename))

    # Sort links alphabetically by title
    song_links.sort(key=lambda x: x[0])

    # Optional: add hearts around a specific song title
    links_html = "\n    ".join(
        f'<li><a href="songs-html/{filename}">{"❤️❤️❤️ " + title + " ❤️❤️❤️" if "Love Story" in title else title}</a></li>'
        for title, filename in song_links
    )

    # ---- Other Resources Section ----
    resources = [
        ("Bluegrass 101 Song Book", "/pdf/bluegrass-101-song-book.pdf"),
        ("The Beatles Complete Songbook", "/pdf/beatles-complete-songbook.pdf"),
        ("The Ultimate Pop Rock Fake Book", "/pdf/ultimate-pop-rock-fake-book.pdf")
        # Add more PDFs here later
    ]

    resource_links_html = ""
    if resources:
        resource_links_html = """
    <h2>Other Resources</h2>
    <ul>
    {}
    </ul>
    """.format("\n".join(
            f'  <li><a href="{url}" target="_blank">{title}</a></li>'
            for title, url in resources
        ))

    # Write index.html in repo root
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX_TEMPLATE.format(
            links=links_html
        ) + resource_links_html)
    print("Site generated in", OUTPUT_DIR)

if __name__ == "__main__":
    generate_site()
