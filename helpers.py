import unidecode
import string
import random
import time
import math
import torch

# Reading and de-unicoding data
all_characters = string.printable
n_characters = len(all_characters)

def read_file(filename):
    # For now, we only intake textfiles
    assert filename.endswith(".txt")
    with open(filename) as file:
        decode_file = unidecode.unidecode(file.read())
        return decode_file, len(decode_file)

# Turning a string into a tensor
def char_tensor(string):
    tensor = torch.zeros(len(string)).long()
    for c in range(len(string)):
        try:
            tensor[c] = all_characters.index(string[c])
        except:
            continue
    return tensor

# Readable time elapsed
def time_since(since):
    s = time.time() - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)