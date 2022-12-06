FROM python:3.9.15-slim-bullseye
WORKDIR /home
EXPOSE 8080
COPY ./setup.sh /
COPY ./requirements.txt /
RUN apt-get update && apt -y install git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r /requirements.txt
ENTRYPOINT ["/setup.sh"]