import torch
import torch.nn as nn
from torch.autograd import Variable

class CharRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout=0.25, model="lstm", n_layers=2):
        super(CharRNN, self).__init__()
        self.model = model.lower()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout = dropout
        self.n_layers = n_layers

        self.encoder = nn.Embedding(num_embeddings=input_size, embedding_dim=hidden_size)
        if self.model == "gru":
            self.rnn = nn.GRU(input_size=hidden_size, hidden_size=hidden_size, num_layers=n_layers)
        elif self.model == "lstm":
            self.rnn = nn.LSTM(input_size=hidden_size, hidden_size=hidden_size, num_layers=n_layers)
        self.decoder = nn.Linear(in_features=hidden_size, out_features=output_size)

    def forward(self, input, hidden):
        batch_size = input.size(0)
        encoded = self.encoder(input)
        output, hidden = self.rnn(encoded.view(1, batch_size, -1), hidden)
        output = self.decoder(output.view(batch_size, -1))
        return output, hidden

    def forward2(self, input, hidden):
        encoded = self.encoder(input.view(1, -1))
        output, hidden = self.rnn(encoded.view(1, 1, -1), hidden)
        output = self.decoder(output.view(1, -1))
        return output, hidden

    def init_hidden(self, batch_size):
        if self.model == "lstm":
            return (Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)),
                    Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)))
        return Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size))