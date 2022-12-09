FROM python:3.9.15-slim-bullseye
WORKDIR /home
EXPOSE 8080
COPY ./setup.sh /
RUN apt-get update && apt -y install git \
    && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/setup.sh"]