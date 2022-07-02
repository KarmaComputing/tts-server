# Text To Speech (TTS) Server setup

Generate `.wav` file from text input.

Using https://github.com/coqui-ai/TTS

This repo shows how to set-up and run your own
TTS server using those models.


## Install / run

Install server requirements (only run on server)
```
./install.sh
```

## Local development

> Note the requirements-api.txt is *not* requirements.txt

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements-api.txt
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

After you have a `ven`, you can also use the shortcut
```
./run.sh
```
## Run Docker container
```
docker pull ghcr.io/karmacomputing/tts-server/tts-server:main
docker run -p 5000:5000 -it tts-server
```

Visit http://127.0.0.1:9090

## Run Docker container from github package
```
docker pull ghcr.io/karmacomputing/tts-server/tts-server:main
docker run -p 9090:9090 -it ghcr.io/karmacomputing/tts-server/tts-server:main
```
Visit http://127.0.0.1:9090

# Example requests

> Note the `lang=` which you can set to the supported language codes
  (see `supported_languages` in `app.py`

Also

> Note: The language models tend to work better with a paragraph or more.
  single world or short phrases less.

## curl

French
```
curl 'https://api.example.com/submit' \
  -H 'authority: api.verby.co' \
  -H 'content-type: application/x-www-form-urlencoded' \
  --data-raw 'text=Le+gros+chien+brun+a+saut%C3%A9+par-dessus+la+b%C3%BBche+paresseuse.&lang=fr' \
  --compressed
```

German `de`
```
curl 'https://api.example.com/submit' \
  -H 'authority: api.verby.co' \
  -H 'cache-control: max-age=0' \
  -H 'content-type: application/x-www-form-urlencoded' \
  --data-raw 'text=Deine+augen+sind+wie+sterne.&lang=de' \
  --compressed
```

## fetch example for French `fr`

French `fr`
```
fetch("https://api.example.com/submit", {
  "headers": {
    "content-type": "application/x-www-form-urlencoded",
    "upgrade-insecure-requests": "1"
  },
  "body": "text=Le+gros+chien+brun+a+saut%C3%A9+par-dessus+la+b%C3%BBche+paresseuse.&lang=fr",
  "method": "POST",
  "mode": "cors",
});
```

# How to I api request the other languages?

Change the `lang` attribute in your api call to a supported language code.
The [language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) currently supported are:

- `en` English
- `de` German
- `es` Spanish
- `fr` French
- `de` German
- `zh-cn` Chinese
- `nl` Dutch (Standard)
- `tr` Turkish
- `it` Italian (Standard)
- `ja` Japanese
