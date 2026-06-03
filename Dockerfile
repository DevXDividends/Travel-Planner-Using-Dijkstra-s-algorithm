# specify a base image
FROM python:3.11-slim

# specify working directory 
WORKDIR /app

## copy the requirement.txt file first !
COPY requirement.txt .

# install all the dependencies
RUN pip install --no-cache-dir -r requirement.txt

## copy all the files into the working dir
COPY . .

## command to run the app
CMD [ "streamlit","run","app.py" ]