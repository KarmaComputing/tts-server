from dotenv import load_dotenv
import os


from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    url_for,
)
import subprocess
from time import time_ns

load_dotenv(verbose=True)

supported_languages = ["en", "de", "zh-cn"]

app = Flask(__name__)
app.config.update(os.environ)

UPLOADS_BATH_PATH = app.config.get("UPLOADS_BATH_PATH")


@app.route("/download/<name>")
def download_file(name):
    return send_from_directory(f"{UPLOADS_BATH_PATH}/", name)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    text_unsafe = request.form.get("text")

    # Set default language model to use
    model_name = "tts_models/en/ljspeech/fast_pitch"
    # Get different language model if possible
    if request.args.get("lang"):
        language = request.args.get("lang").lower()
        if language in supported_languages:
            # wip default to de
            # see github.com/KarmaComputing/tts-server/issues/14
            model_name = "tts_models/de/thorsten/tacotron2-DCA"

    filename = f"{time_ns()}.wav"

    # WARNING this is unsafe, see shell.escape
    subprocess.run(
        f'tts --text "{text_unsafe}" --out_path "{UPLOADS_BATH_PATH}/{filename}" --model_name {model_name}',  # noqa: E501
        shell=True,
    )
    return redirect(url_for("download_file", name=filename))
