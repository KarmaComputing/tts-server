# Test To Speech (TTS) Server setup

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
## Run Docker container
```
cd tts-server/
docker build -t tts-server .
docker run -p 5000:5000 -it tts-server
```

Visit http://127.0.0.1:5000
