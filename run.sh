#!/bin/bash
uwsgi --http :9090 --wsgi-file app.wsgi
