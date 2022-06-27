#!/bin/bash

export FLASK_APP=app
export FLASK_DEBUG=1
. venv/bin/activate
flask run
