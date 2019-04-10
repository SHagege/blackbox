#!/bin/bash

pip3 install -r requirements.txt
cd explorer/
python3 manage.py makemigrations
python3 manage.py migrate