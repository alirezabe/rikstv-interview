FROM python:3.11-slim
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app/
COPY main.py .
COPY config.py .
COPY start.sh .
COPY gunicorn_conf.py .
RUN chmod +x /app/start.sh
ENV PYTHONPATH=/app
ENV MAX_WORKERS=4
CMD ["gunicorn -k uvicorn.workers.UvicornWorker -c /app/gunicorn_conf.py main:app"]