# 1721-Bingo

![image](https://github.com/user-attachments/assets/e22b2cce-e806-4abf-95a2-0282685c56df)

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

Sheets are generated randomly, edit `bingo_data.yaml` when you want more/less.
