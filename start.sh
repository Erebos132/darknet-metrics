#!/bin/bash
cd /home/bendix/darknet-metrics
source venv/bin/activate
gunicorn -w 1 app:app -b 127.0.0.1:5000
