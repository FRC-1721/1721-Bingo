import argparse
import random
import os
import yaml

from pathlib import Path
from PyPDF2 import PdfMerger

# Define paths
TEMPLATE_FILE = "bingosheet.tex"
RENDERS_DIR = Path("renders")
BINGO_DATA_FILE = "bingo_data.yaml"

# Ensure renders directory exists
RENDERS_DIR.mkdir(exist_ok=True)


def load_squares():
    """Load bingo square suggestions from a YAML file."""
    with open(BINGO_DATA_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_bingo_card(template: str, bingo_data: dict) -> str:
    """Replace the AUTOPOP ANCHOR in the template with randomized, generated replacements."""
    normal_squares = bingo_data.get("NORMAL", [])
    special_squares = {
        "FREE": bingo_data.get("FREE", []),
        "MENTOR": bingo_data.get("MENTOR", []),
        "ALUMNI": bingo_data.get("ALUMNI", []),
        "PLUMB": bingo_data.get("PLUMB", []),
        "CAPTAIN": bingo_data.get("CAPTAIN", []),
    }

    random.shuffle(normal_squares)

    # Special cell placements
    special_positions = {
        (2, 2): ("darkgrey", "FREE SPACE", "AUTOPOP FREE"),
        (2, 0): ("maroon", "MENTOR SPACE", "AUTOPOP MENTOR"),
        (4, 2): ("lightgrey", "ALUMNI SPACE", "AUTOPOP ALUMNI"),
        (2, 4): ("purple", "PLUMB SPACE", "AUTOPOP PLUMB"),
        (0, 2): ("gold", "CAPTAIN SPACE", "AUTOPOP CAPTAIN"),
    }

    # Generate LaTeX nodes for special squares
    special_nodes = []
    for (col, row), (color, title, placeholder) in special_positions.items():
        subtitle = (
            random.choice(special_squares[title.split()[0]])
            if special_squares[title.split()[0]]
            else ""
        )
        special_nodes.append(
            f"\\specialcell{{{col}}}{{{row}}}{{{color}}}{{{title}}}{{{subtitle}}};"
        )

    # Generate LaTeX nodes for normal squares
    normal_index = 0
    normal_nodes = []
    for row in range(5):
        for col in range(5):
            if (row, col) not in special_positions:
                square_text = normal_squares[normal_index]
                normal_index += 1
                normal_nodes.append(
                    f"\\node[thick, text width=3cm, align=center] at ({col}, -{row}) {{{square_text}}};"
                )

    # Replace AUTOPOP ANCHOR with both normal and special nodes
    populated_template = template.replace(
        "% {AUTOPOP ANCHOR}", "\n".join(special_nodes + normal_nodes)
    )

    return populated_template


def stitch_pdfs():
    """Stitch all generated PDFs into a single document."""
    pdfs = sorted(RENDERS_DIR.glob("*.pdf"))
    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(str(pdf))

    stitched_output = "stitched_bingo.pdf"
    merger.write(stitched_output)
    merger.close()

    print(f"All PDFs stitched into {stitched_output}")


def main(n: int, stitch: bool):
    """Generate n bingo sheets."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    bingo_data = load_squares()

    for i in range(n):
        bingo_tex = generate_bingo_card(template, bingo_data)
        output_path = RENDERS_DIR / f"bingo_{i+1}.tex"
        pdf_output_path = RENDERS_DIR / f"bingo_{i+1}.pdf"

        # Save LaTeX file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(bingo_tex)

        # Compile to PDF
        os.system(f"pdflatex -output-directory={RENDERS_DIR} {output_path}")

        print(f"Generated {pdf_output_path}")

    if stitch:
        stitch_pdfs()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random bingo sheets.")
    parser.add_argument(
        "-n", type=int, default=1, help="Number of bingo sheets to generate"
    )
    parser.add_argument(
        "-s", action="store_true", help="Stitch all PDFs into one document"
    )
    args = parser.parse_args()
    main(args.n, args.s)
