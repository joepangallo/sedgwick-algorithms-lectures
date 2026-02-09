#!/usr/bin/env python3
"""Convert lecture markdown files to styled PDFs matching the Sedgwick lecture format."""

import os
import glob
import markdown
from weasyprint import HTML

LECTURES_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.dirname(LECTURES_DIR)  # Parent dir (repo root)

CSS = """
@page {
    size: letter;
    margin: 1in 0.85in;
    @bottom-center {
        content: "Page " counter(page);
        font-size: 8pt;
        color: #666;
    }
}

@page :first {
    margin-top: 2in;
}

body {
    font-family: "Georgia", "Times New Roman", "DejaVu Serif", serif;
    font-size: 11pt;
    line-height: 1.65;
    color: #1a1a1a;
}

h1 {
    font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 13pt;
    color: #444;
    text-transform: uppercase;
    letter-spacing: 3px;
    text-align: center;
    margin-top: 0;
    margin-bottom: 4px;
    font-weight: 400;
}

h2 {
    font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 22pt;
    color: #1a1a1a;
    text-align: center;
    margin-top: 0;
    margin-bottom: 20px;
    font-weight: 700;
    line-height: 1.2;
}

h2 + p > strong:first-child {
    display: block;
    text-align: center;
    font-size: 12pt;
    color: #333;
}

h3 {
    font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 15pt;
    color: #1a3a6b;
    margin-top: 28px;
    margin-bottom: 10px;
    border-bottom: 2px solid #1a3a6b;
    padding-bottom: 4px;
}

h4 {
    font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 12pt;
    color: #2a5a9b;
    margin-top: 20px;
    margin-bottom: 8px;
}

p {
    margin-bottom: 10px;
    text-align: justify;
}

code {
    font-family: "SFMono-Regular", "Fira Code", Consolas, "Liberation Mono", monospace;
    font-size: 9.5pt;
    background-color: #f0f2f5;
    padding: 1px 4px;
    border-radius: 3px;
    color: #c7254e;
}

pre {
    background-color: #1e293b;
    color: #e2e8f0;
    padding: 14px 16px;
    border-radius: 4px;
    margin: 12px 0;
    line-height: 1.45;
    page-break-inside: avoid;
}

pre code {
    background: transparent;
    color: #e2e8f0;
    padding: 0;
    font-size: 9pt;
}

ul, ol {
    margin-bottom: 10px;
    padding-left: 22px;
}

li {
    margin-bottom: 4px;
}

blockquote {
    border-left: 3px solid #1a3a6b;
    margin: 14px 0;
    padding: 10px 16px;
    background-color: #f0f4f8;
    font-style: italic;
}

blockquote p {
    margin: 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

th, td {
    border: 1px solid #c8ccd0;
    padding: 7px 10px;
    text-align: left;
}

th {
    background-color: #1a3a6b;
    color: white;
    font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    font-weight: 600;
    font-size: 9.5pt;
}

tr:nth-child(even) {
    background-color: #f8f9fa;
}

strong {
    color: #111;
}

em {
    color: #333;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 24px 0;
}

a {
    color: #1a3a6b;
    text-decoration: none;
}

/* Footer line */
.footer-line {
    font-size: 8pt;
    color: #888;
    text-align: center;
    margin-top: 20px;
}
"""


def convert_md_to_pdf(md_path, pdf_path, lecture_num):
    """Convert a lecture markdown file to PDF."""
    with open(md_path, "r") as f:
        md_content = f.read()

    html_content = markdown.markdown(
        md_content,
        extensions=["fenced_code", "tables", "toc", "codehilite", "nl2br"],
    )

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>{CSS}</style>
</head>
<body>
{html_content}
</body>
</html>"""

    HTML(string=full_html).write_pdf(pdf_path)
    print(f"  Created: {os.path.basename(pdf_path)}")


def main():
    md_files = sorted(glob.glob(os.path.join(LECTURES_DIR, "Lecture-*.md")))

    if not md_files:
        print("No lecture markdown files found!")
        return

    print(f"Found {len(md_files)} lecture files. Converting to PDF...\n")

    success = 0
    for md_path in md_files:
        basename = os.path.basename(md_path)
        num = basename.split("-")[1].split(".")[0]
        pdf_name = f"Lecture-{num}.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
        try:
            convert_md_to_pdf(md_path, pdf_path, num)
            success += 1
        except Exception as e:
            print(f"  ERROR converting {basename}: {e}")

    print(f"\nDone! {success}/{len(md_files)} PDFs created in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
