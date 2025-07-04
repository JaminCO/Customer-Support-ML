# Base Image
FROM python:3.10-slim

# Install required system packages
# RUN apt-get update && apt-get clean

# set environment variables

# set working directory

WORKDIR /code

# add and install requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

# add app
COPY ./ /code/

# run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]