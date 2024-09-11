FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY . /app/

WORKDIR /app/library

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

