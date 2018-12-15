# This is a simple, unintelligent parser for Cornell's movie_lines.txt file.
# It grabs only the dialogue lines (i.e., no metadata), and splices them together back-to-back.
import os
import re
import string
import unidecode

input_filepath = "data/CMU-movie-summary-corpus/plot_summaries.txt"
output_filepath = "data/cmu_movie_summary_parse.txt"

trash = ["{{Expand section}}", "{{expand section}}", "{{plot}}", "{{Plot}}", "{{cquote}}", "{{cite web}}", "{{Cite web}}", "{{cite news}}", "{{Cite news}}", "{{tone}}", "{{Amg movie}}", "{{long plot}}", "{{cite book}}", "{{Cite book}}", "{{citation needed}}", "{{INR}}", "{{Ref_label}}", "{{Fact}}", "{{quote}}", "{{Quote}}", "{{more plot}}"]

# Defines allowed punctuation, letters, numbers, and whitespace, respectively
accepted_characters = ".,:;?!-()[]" + string.ascii_letters + string.digits + " \n"
accepted_set = set(accepted_characters)

with open(input_filepath, encoding="utf-8", errors="ignore") as input_file:
	with open(output_filepath, "w", encoding="ascii") as output_file:
		for i, line in enumerate(input_file):
			line = unidecode.unidecode(line)
			line = re.sub(r"^\d+\w*", "", line)
			line = line.strip()

			for t in trash:
				line = line.replace(t, "")

			line = line.replace("{{mdash}}", " - ")
			if line and set(line) <= accepted_set:
				# Sadly, we do not accept lines with link spam, at all
				if "http://" not in line and "https://" not in line:
					output_file.write("$$BEGIN$$ " + line + "\n")
