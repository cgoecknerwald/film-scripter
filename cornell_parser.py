# This is a simple, unintelligent parser for Cornell's movie_lines.txt file.
# It grabs only the dialogue lines (i.e., no metadata), and splices them together back-to-back.
import os
import unidecode

input_filepath = "data/cornell-movie-dialogs-corpus/movie_lines.txt"
output_filepath = "data/cornell_movie_lines_parse.txt"

with open(input_filepath, encoding="utf-8", errors="ignore") as input_file:
	with open(output_filepath, "w", encoding="ascii") as output_file:
		for i, line in enumerate(input_file):
			line = unidecode.unidecode(line).split('+++$+++')[4].replace("  ", " ").strip()
			if line:
				output_file.write(line + "\n")
