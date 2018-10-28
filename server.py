import os
import torch

from flask import Flask, render_template, jsonify
from generate import generate

app = Flask(__name__, template_folder="docs", static_folder="docs/static")

@app.route("/")
def index():
    return render_template("index.html")

# Handle calls to generate text from a pre-trained model
@app.route("/generator")
def generator():
	# Hard-coded pre-trained model
	decoder = torch.load("models/plot_summaries.pt")
	output = generate(decoder, prime_str='Where ', predict_len=500, temperature=0.6, cuda=False)
	return jsonify({'text': output})

# Hacky way to shut down the app
@app.route("/shutdown")
def shutdown():
	os._exit(0)

if __name__ == "__main__":
	# Uncomment to debug the app. Beware of debug-mode security issues
	# app.debug = True
	app.run()
