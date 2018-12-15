#!/usr/bin/env python

import torch
import torch.nn as nn
from torch.autograd import Variable
import argparse
import os
import pathlib

from tqdm import tqdm

from helpers import *
from model import *
from generate import *

# Parse command line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument('pathname', type=str)
argparser.add_argument('--model', type=str, default="gru")
argparser.add_argument('--n_epochs', type=int, default=1000)
argparser.add_argument('--print_every', type=int, default=100)
argparser.add_argument('--hidden_size', type=int, default=100)
argparser.add_argument('--n_layers', type=int, default=2)
argparser.add_argument('--learning_rate', type=float, default=0.01)
argparser.add_argument('--chunk_len', type=int, default=200)
argparser.add_argument('--batch_size', type=int, default=100)
argparser.add_argument('--shuffle', action='store_true')
argparser.add_argument('--cuda', action='store_true')
args = argparser.parse_args()

if args.cuda:
    print("Using CUDA")

def build_file_dict(pathname):
    # Dict{string: [string, int]}
    file_dict = {}
    # Accept a single file
    if os.path.isfile(pathname):
        file, file_len = read_file(pathname)
        file_dict[pathname] = [file, file_len]
    # Alternately, accept a directory of files
    else:
        assert(os.path.isdir(pathname)), "Given pathname {} must be valid directory or file".format(pathname)
        for f in os.listdir(pathname):
            filename = os.path.join(pathname, os.fsdecode(f))
            try:
                file, file_len = read_file(filename)
                file_dict[filename] = [file, file_len]
            except Exception as e:
                print("Exception: {} caused failure to read file '{}'".format(e, filename))
                continue
    # Assert non-empty dictionary of files
    assert file_dict, "Function build_file_dict found no valid file(s) at {}".format(pathname)
    return file_dict


def random_training_set(file_dict, chunk_len, batch_size):
    inp = torch.LongTensor(batch_size, chunk_len)
    target = torch.LongTensor(batch_size, chunk_len)
    # TODO: Make a more flexible batching algorithm to accomodate complete words.
    for bi in range(batch_size):
        # Select from a random file in our file_dict
        while True:
            try:
                file, file_len = random.choice(list(file_dict.values()))
                start_index = random.randint(0, file_len - chunk_len)
                end_index = start_index + chunk_len + 1
                chunk = file[start_index:end_index]
                inp[bi] = char_tensor(chunk[:-1])
                target[bi] = char_tensor(chunk[1:])
            except RuntimeError as e:
                print(e)
                print("Error in train.random_training_set(). Trying again...")
            else:
                break
    inp = Variable(inp)
    target = Variable(target)
    if args.cuda:
        inp = inp.cuda()
        target = target.cuda()
    return inp, target

def train(inp, target):
    hidden = decoder.init_hidden(args.batch_size)
    if args.cuda:
        hidden = hidden.cuda()
    decoder.zero_grad()
    loss = 0

    for c in range(args.chunk_len):
        output, hidden = decoder(inp[:,c], hidden)
        loss += criterion(output.view(args.batch_size, -1), target[:,c])

    loss.backward()
    decoder_optimizer.step()

    # Use tensor.item
    return loss.data.item() / args.chunk_len

def save():
    subdir = 'models/'
    file_ext = ".pt"

    # Create 'models/' subdirectory if it does not already exist
    pathlib.Path(subdir).mkdir(parents=True, exist_ok=True)

    # Modelname is the dirname for directorys and the filename for files
    modelname = os.path.basename(args.pathname.rstrip('/'))
    modelname = os.path.splitext(modelname)[0]
    # Model names should have no punctuation or whitespace; only alphanumeric
    # We also convert to lowercase and trim to the first 15 characters
    modelname = ''.join(e for e in modelname if e.isalnum()).lower()[:15]
    # Include model type, n_epochs, n_layers, hidden size, learning rate
    modelname = modelname + '_' + args.model.upper() + '_NE' + str(args.n_epochs) \
                          + '_NL' + str(args.n_layers) + '_HS' + str(args.hidden_size)

    save_filename = subdir + modelname + file_ext
    torch.save(decoder, save_filename)
    print('Saved as %s' % save_filename)

# Initialize models and start training
decoder = CharRNN(
    n_characters,
    args.hidden_size,
    n_characters,
    model=args.model,
    n_layers=args.n_layers,
)
decoder_optimizer = torch.optim.Adam(decoder.parameters(), lr=args.learning_rate)
criterion = nn.CrossEntropyLoss()

if args.cuda:
    decoder.cuda()

start = time.time()
all_losses = []
loss_avg = 0

try:
    # Dict{string: [string, int]}
    file_dict = build_file_dict(args.pathname)
    print("Found files: {}".format(list(file_dict.keys())))
    print("Training for %d epochs..." % args.n_epochs)
    for epoch in tqdm(range(1, args.n_epochs + 1)):
        loss = train(*random_training_set(file_dict, args.chunk_len, args.batch_size))
        loss_avg += loss
        if epoch % args.print_every == 0:
            print('[%s (%d %d%%) %.4f]' % (time_since(start), epoch, epoch / args.n_epochs * 100, loss))
            print(generate(decoder, 'Wh', 100, cuda=args.cuda), '\n')

    print("Saving...")
    # TODO: close all files
    save()

except KeyboardInterrupt:
    print("Saving before quit...")
    # TODO: close all files
    save()

