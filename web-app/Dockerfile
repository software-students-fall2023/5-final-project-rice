FROM python:3.11

WORKDIR /web-app

COPY web-app/requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt

COPY . /web-app

EXPOSE 3000


# Run app.py when the container launches

COPY . /app

EXPOSE 3000

CMD ["python", "app.py"]