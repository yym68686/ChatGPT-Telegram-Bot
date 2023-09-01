FROM python:3.10.13-slim-bullseye
WORKDIR /home
EXPOSE 8080
COPY ./setup.sh /home
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/home/setup.sh"]