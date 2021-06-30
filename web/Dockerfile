FROM python:3.7-slim

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt

# install requirements in image
RUN python -m pip install -r requirements.txt

# copy content in folder
COPY  . .

RUN coverage run testcases.py
RUN coverage report -m src/controllers/*.py
RUN coverage html src/controllers/*.py