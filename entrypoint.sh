#!/bin/bash
uwsgi --http 0.0.0.0:9090 --wsgi-file /code/app.py --callable app

