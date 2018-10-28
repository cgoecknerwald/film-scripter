# film-scripter
Deep Learning 02456 Project (Denmark Technical University)
Fall 2018

### The Dataset

You can find the main dataset on [figshare](https://figshare.com/projects/imsdb_movie_scripts/18907), courtesy of [Alberto Acerbi](https://acerbialberto.com/). This dataset contains 1,093 popular movie scripts.

### Usage

The folder `shakespeare` is a dataset of Shakespeare's plays. To run the server,

```
python3.6 -m pip install Flask
python3.6 server.py
```

The website is locally hosted at `http://127.0.0.1:5000/`.

To shutdown, visit

```
http://127.0.0.1:5000/shutdown
```

or click the shutdown button.

### Thanks

The base of this repository was borrowed from [Sean Robertson's](https://github.com/spro) [char-rnn.pytorch](https://github.com/spro/char-rnn.pytorch) under the MIT License.

The model is based on Andrej Karpathy's popular [char-rnn](https://github.com/karpathy/char-rnn), which is described in detail on his [blogpost](https://karpathy.github.io/2015/05/21/rnn-effectiveness/).

The practice dataset in `shakespeare` comes from [Ravexina's](https://github.com/ravexina) [shakespeare-plays-dataset-scraper](https://github.com/ravexina/shakespeare-plays-dataset-scraper).

[Background image](https://unsplash.com/photos/evlkOfkQ5rE) taken from Unsplash's [Felix Mooneeram](https://unsplash.com/@felixmooneeram). 