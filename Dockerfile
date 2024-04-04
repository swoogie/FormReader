FROM python:3.11.8-alpine3.18

WORKDIR /app

RUN apk add --update tesseract-ocr tesseract-ocr-data-eng tesseract-ocr-data-osd py3-opencv

RUN apk cache clean

ENV PYTHONPATH='$PYTHONPATH:/usr/lib/python3.11/site-packages'

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "server/app.py"]
