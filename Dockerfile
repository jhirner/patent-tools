# set base image (host OS)
FROM python:3.9-slim-buster

# set the working directory in the container
WORKDIR /source

# copy the dependencies file to the working directory
COPY requirements.txt .

# copy the content of the local source directory to the working directory
COPY patenttools/ /source/

# install dependencies
RUN pip install -r requirements.txt
RUN python3 install_nltk_punkt.py

# Run the production-ready server
CMD ["gunicorn", "frontend:app"]

# Run the development server
#CMD ["python3", "frontend.py"]