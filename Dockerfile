FROM python:2.7

COPY db.py /app/db.py

WORKDIR /app

CMD ["python", "db.py"]
