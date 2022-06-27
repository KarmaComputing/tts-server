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

supported_languages = ["en", "de", "fr", "zh-cn", "es", "nl", "tr", "it", "ja"]

# Map the ISO 639-1 language code to a model which supports that language
# Note: Some languages have multiple models to choose from, this is simpler
# on purpose to satisfy https://github.com/KarmaComputing/tts-server/issues/14
# and can be extended in future
language_to_model = {
    "de": "tts_models/de/thorsten/tacotron2-DCA",
    "en": "tts_models/de/thorsten/tacotron2-DCA",
    "fr": "tts_models/fr/mai/tacotron2-DDC",
    "zh-cn": "tts_models/zh-CN/baker/tacotron2-DDC-GST",
    "es": "tts_models/es/mai/tacotron2-DDC",
    "nl": "tts_models/nl/mai/tacotron2-DDC",
    "tr": "tts_models/tr/common-voice/glow-tts",
    "it": "tts_models/it/mai_female/glow-tts",
    "ja": " 19: tts_models/ja/kokoro/tacotron2-DDC",
}

app = Flask(__name__)
app.config.update(os.environ)

UPLOADS_BATH_PATH = app.config.get("UPLOADS_BATH_PATH")
TTS_PATH = app.config.get("TTS_PATH")


@app.route("/download/<name>")
def download_file(name):
    return send_from_directory(f"{UPLOADS_BATH_PATH}/", name)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST", "GET"])
def submit():
    text_unsafe = request.form.get("text")

    # Set default language model to use
    model_name = "tts_models/en/ljspeech/fast_pitch"
    # Get different language model if possible

    # Get requested_language from get arg if present
    requested_language = request.args.get("lang", None)
    if requested_language is None:
        requested_language = request.form.get("lang", None)

    # Attempt to get
    if requested_language is not None:
        language = requested_language.lower()
    else:
        language = "en"

    print(f"Attemping to use language {language}")
    if language in supported_languages:
        model_name = language_to_model[language]
        print(f"Model name set to: {model_name}")
    else:
        print(f"Could not locate model for requested language: {language}")

    print(f"Model name is set to: {model_name}")

    filename = f"{time_ns()}.wav"

    # WARNING this is unsafe, see shell.escape
    subprocess.run(
        f'{TTS_PATH} --text "{text_unsafe}" --out_path "{UPLOADS_BATH_PATH}/{filename}" --model_name {model_name}',  # noqa: E501
        shell=True,
    )
    return redirect(url_for("download_file", name=filename))
