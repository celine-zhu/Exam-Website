#!/bin/bash
python3 -m venv env 
source env/bin/activate 
pip3 install Flask 
pip3 install Flask-Images
pip3 install geopandas
pip3 install pdfkit
echo 'env/' >> .gitignore  
pip3 freeze 
pip3 freeze > requirements.txt 
pip3 install -r requirements.txt 
pip3 install click
deactivate
sudo apt-get install wkhtmltopdf
exit $?