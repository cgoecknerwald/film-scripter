# This is a simple, unintelligent parser for Gutenberg's textfiles
import os
import re
import string
import unidecode

input_filepath = "data/gutenberg/"
output_filepath = "data/gutenberg_parse.txt"

first_person = ["I", "I'm", "I've", "I'd", "I'll"]

# Defines allowed punctuation, letters, numbers, and whitespace, respectively
accepted_characters = ".,:;?!-" + string.ascii_letters + string.digits + " \n"
accepted_set = set(accepted_characters)

# TODO: trim line numbers
# TODO: stop making orphan sentences
# TODO: no newline immediately after spaces or letters

with open(output_filepath, "w", encoding="ascii") as output_file:
    for filename in os.listdir(input_filepath):
        filepath = os.path.join(input_filepath, filename)
        print("Reading:", filepath)
        if os.path.isfile(filepath):
            with open(filepath, encoding="utf-8", errors="ignore") as input_file:
                # Whether or not this line should begin with capitalization
                next_line_caps = True
                # Loop until the actual text starts (indicated by Gutenberg with "***")
                for line in input_file:
                    if "***" in line:
                        break
                # Reading actual text
                for line in input_file:
                    # We have reached the end of the Gutenberg text. Licensing follows.
                    if "***" in line:
                        break

                    line = unidecode.unidecode(line)
                    # Some lines may end with a line number. Remove, then strip.
                    line = re.sub(r"\w*\d+$", "", line)
                    line = line.strip()
                    # Update weird ellipses (in this order)
                    line = line.replace(" . . .", " ...")
                    line = line.replace(". . . ", "... ")
                    line = line.replace("....", ".")
                    # Change double-spacing to single-spacing and remove underscore (used for italics)
                    line = line.replace("  ", " ").replace("_", "")
                    # Do not consider lines that are all caps and numbers.
                    # There may be additional "Gutenberg" tagging as well, which we can ignore.
                    if line and set(line) <= accepted_set and not line.isupper() and "Gutenberg" not in line:
                        if next_line_caps == True:
                            line = line[0].upper() + line[1:]
                        else:
                            line = line[0].lower() + line[1:]
                        # If the line ends with a letter, comma, colon, or semicolon, remove newline.
                        # AKA: newlines are OK after .?!
                        if line[-1] in "?.!":
                            output_file.write(line + "\n")
                            next_line_caps = True
                        else:
                            output_file.write(line + " ")
                            next_line_caps = False

