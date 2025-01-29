# 1721-Bingo

```shell
$ bingo.py
usage: bingo.py [-h] [-n N] [-s]

Generate random bingo sheets.

options:
  -h, --help  show this help message and exit
  -n N        Number of bingo sheets to generate
  -s          Stitch all PDFs into one document
```

Usage is simple! You must have `pdflatex` installed to generate.

`python bingo.py -n <number of sheets> -s`

Sheets are generated randomly, edit bingo_squares.txt when you want more/less.
