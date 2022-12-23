FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "pets.wsgi", "--bind", "0:8000"]
