import argparse
import random
import os
from pathlib import Path

# Define paths
TEMPLATE_FILE = "bingosheet.tex"
RENDERS_DIR = Path("renders")
BINGO_SQUARES_FILE = "bingo_squares.txt"

# Ensure renders directory exists
RENDERS_DIR.mkdir(exist_ok=True)


def load_squares():
    """Load bingo square suggestions from a text file."""
    with open(BINGO_SQUARES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def generate_bingo_card(template: str, squares: list[str]) -> str:
    """Replace the AUTOPOP ANCHOR in the template with randomized squares."""
    random.shuffle(squares)
    selected_squares = squares[:25]
    selected_squares[12] = ""  # Center free space

    # Generate LaTeX nodes for each square
    nodes = []
    for i, square in enumerate(selected_squares):
        row, col = divmod(i, 5)
        nodes.append(
            f"\\node[thick, text width=3.1cm, align=center] at ({col}, -{row}) {{{square}}};"
        )

    # Replace the AUTOPOP ANCHOR with generated nodes
    populated_template = template.replace("% {AUTOPOP ANCHOR}", "\n".join(nodes))
    return populated_template


def main(n: int):
    """Generate n bingo sheets."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    squares = load_squares()
    for i in range(n):
        bingo_tex = generate_bingo_card(template, squares)
        output_path = RENDERS_DIR / f"bingo_{i+1}.tex"
        pdf_output_path = RENDERS_DIR / f"bingo_{i+1}.pdf"

        # Save LaTeX file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(bingo_tex)

        # Compile to PDF
        os.system(f"pdflatex -output-directory={RENDERS_DIR} {output_path}")

        print(f"Generated {pdf_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random bingo sheets.")
    parser.add_argument(
        "-n", type=int, default=1, help="Number of bingo sheets to generate"
    )
    args = parser.parse_args()
    main(args.n)
