FROM python:3.9-alpine3.13
LABEL maintainer="pedrocantu.com"

#prevents any delays in logs
#because of buffering
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

#by default value of DEV is false
ARG DEV=false

#create a virtual environment and install dependencies
#each RUN creates a new layer making the image larger
#so we chain commands using && to keep it in one layer
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [  $DEV = "true" ];\
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

#uptades the environment path to use the virtualenv
#this way we don't have to use the full path to python or pip
ENV PATH="/py/bin:$PATH"

#prevent running as root
#switch to a non-privileged user
#this user was created in the RUN command above
#and prevents security issues
USER django-user