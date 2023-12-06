FROM python:3.11

WORKDIR /web-app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get -y install libasound-dev
RUN apt-get -y install portaudio19-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . /web-app

EXPOSE 5000


# Run app.py when the container launches

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]