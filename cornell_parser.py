# This is a simple, unintelligent parser for Cornell's movie_lines.txt file.
# It grabs only the dialogue lines (i.e., no metadata), and splices them together back-to-back.
import os
import string
import unidecode

input_filepath = "data/cornell-movie-dialogs-corpus/movie_lines.txt"
output_filepath = "data/cornell_movie_lines_parse.txt"

# Defines allowed punctuation, letters, numbers, and whitespace, respectively
accepted_characters = ".,:;?!-" + string.ascii_letters + string.digits + " \n"
accepted_set = set(accepted_characters)

with open(input_filepath, encoding="utf-8", errors="ignore") as input_file:
	with open(output_filepath, "w", encoding="ascii") as output_file:
		for i, line in enumerate(input_file):
			line = unidecode.unidecode(line).split('+++$+++')[4].replace("  ", " ").strip()
			if line and set(line) <= accepted_set:
				output_file.write(line + "\n")
