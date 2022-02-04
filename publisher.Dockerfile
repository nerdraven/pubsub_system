FROM python:3.9.2-slim

ENV PYTHONUNBUFFERED=x

WORKDIR /tmp



COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app

COPY protocol protocol
COPY publisher publisher

CMD exec gunicorn -b 0.0.0.0:${PORT} publisher.main:app