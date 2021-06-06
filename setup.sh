#!/bin/sh
pip install gdown 
gdown --id 1I7OjhaomWqd8Quf7o5suwLloRlY0THbp
mkdir WiderPerson
unzip WiderPerson.zip -d WiderPerson/
rm WiderPerson.zip
python setup_wp_dataset.py 