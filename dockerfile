FROM python:3.11

ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput
