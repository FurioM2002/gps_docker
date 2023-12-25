FROM python:3.12-alpine3.18

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev mariadb-dev python3-dev libffi-dev \
    && pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

WORKDIR /app/crud_gps

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]