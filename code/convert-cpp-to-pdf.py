#!/usr/bin/env python3
"""Convert C++ source files to syntax-highlighted PDFs using Pygments + WeasyPrint."""

import os
import glob
from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter
from weasyprint import HTML

CODE_DIR = os.path.dirname(os.path.abspath(__file__))

CSS = """
@page {
    size: letter;
    margin: 0.75in 0.6in;
    @bottom-center {
        content: "Page " counter(page);
        font-size: 8pt;
        color: #888;
    }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    font-size: 10pt;
    color: #1a1a1a;
    margin: 0;
}

.header {
    background: linear-gradient(135deg, #1e3a5f, #2563eb);
    color: white;
    padding: 16px 20px;
    margin: -0.75in -0.6in 20px -0.6in;
    width: calc(100% + 1.2in);
}

.header h1 {
    font-size: 16pt;
    margin: 0 0 4px 0;
    font-weight: 700;
}

.header p {
    font-size: 9pt;
    margin: 0;
    opacity: 0.85;
}

.highlight {
    font-size: 8.5pt;
    line-height: 1.45;
}

.highlight pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    background: #f8f9fa;
    padding: 12px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}
"""

# Lecture titles for headers
TITLES = {
    "01": "Introduction, Algorithm Analysis, Big-O Notation",
    "02": "Elementary Data Structures (Arrays, Linked Lists, Stacks, Queues)",
    "03": "Elementary Sorting (Selection, Insertion, Shellsort)",
    "04": "Mergesort and Quicksort",
    "05": "Priority Queues and Heapsort",
    "06": "Binary Search Trees",
    "07": "Balanced Search Trees (Red-Black BSTs)",
    "08": "Hash Tables",
    "09": "Graph Fundamentals and Depth-First Search",
    "10": "Breadth-First Search and Graph Applications",
    "11": "Minimum Spanning Trees and Shortest Paths",
    "12": "Advanced Topics (String Algorithms, Tries, Dynamic Programming)",
}


def convert_cpp_to_pdf(cpp_path, pdf_path):
    """Convert a C++ source file to a syntax-highlighted PDF."""
    with open(cpp_path, "r") as f:
        code = f.read()

    # Extract lecture number from filename
    basename = os.path.basename(cpp_path)
    num = basename.split("-")[1] if "-" in basename else "00"
    title = TITLES.get(num, "Code Samples")

    # Syntax highlight with Pygments
    lexer = CppLexer()
    formatter = HtmlFormatter(
        style="monokai",
        noclasses=True,
        nowrap=False,
    )
    highlighted = highlight(code, lexer, formatter)

    # Build HTML
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>{CSS}</style>
</head>
<body>
    <div class="header">
        <h1>Lecture {num}: {title}</h1>
        <p>C++ Code Samples &mdash; Sedgwick Algorithms Course &mdash; {basename}</p>
    </div>
    <div class="highlight">
        {highlighted}
    </div>
</body>
</html>"""

    HTML(string=full_html).write_pdf(pdf_path)
    print(f"  Created: {os.path.basename(pdf_path)}")


def main():
    cpp_files = sorted(glob.glob(os.path.join(CODE_DIR, "lecture-*-samples.cpp")))

    if not cpp_files:
        print("No C++ sample files found!")
        return

    print(f"Found {len(cpp_files)} C++ files. Converting to PDF...\n")

    success = 0
    for cpp_path in cpp_files:
        pdf_path = cpp_path.replace(".cpp", ".pdf")
        try:
            convert_cpp_to_pdf(cpp_path, pdf_path)
            success += 1
        except Exception as e:
            print(f"  ERROR converting {os.path.basename(cpp_path)}: {e}")

    print(f"\nDone! {success}/{len(cpp_files)} PDFs created.")


if __name__ == "__main__":
    main()
