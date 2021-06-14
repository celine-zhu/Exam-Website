#!/bin/bash

source ProjectEnvironnement/bin/activate 
cd src/appli
export FLASK_APP=Appli.py
export FLASK_ENV=development
xdg-open http://127.0.0.1:5000/
flask run
deactivate
