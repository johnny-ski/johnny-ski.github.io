
from pathlib import Path
from html import escape
from urllib.parse import quote

SITE_URL = "https://johnny-ski.github.io"

# Folders to include in the directory.
FOLDERS = [
    ("Song Pages", "songs-html"),
    ("PDFs and Documents", "pdf"),
    ("In-Progress Songs", "in-progress"),
    ("Images", "images"),
    ("Song Source Text", "songs-text"),
]

OUTPUT_FILE = Path("site-map.html")

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Private Site Directory</title>
<style>
body {
    font-family: monospace;
    max-width: 700px;
    margin: 30px auto;
    padding: 0 20px;
    line-height: 1.6;
}
h1, h2 {
    margin-top: 30px;
}
li {
    margin-bottom: 6px;
}
a {
    color: #0645ad;
}
</style>
</head>
<body>
<h1>Site Directory</h1>
<p>Directory of songs, documents, and other website resources.</p>
"""

for title, folder in FOLDERS:
    directory = Path(folder)

    if not directory.exists():
        continue

    files = sorted(
        p for p in directory.rglob("*")
        if p.is_file()
        and not p.name.startswith(".")
        and p.suffix.lower() not in (".save", ".bak", ".swp")
    )

    if not files:
        continue

    html += f"\n<h2>{escape(title)}</h2>\n<ul>\n"

    for file in files:
        relative_path = file.as_posix()
        url = SITE_URL + "/" + quote(relative_path, safe="/")
        label = relative_path

        html += (
            f'<li><a href="{escape(url, quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">'
            f'{escape(label)}</a></li>\n'
        )

    html += "</ul>\n"

html += """
</body>
</html>
"""

OUTPUT_FILE.write_text(html, encoding="utf-8")
print(f"Created {OUTPUT_FILE}")
