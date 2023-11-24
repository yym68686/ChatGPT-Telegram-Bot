FROM python:3.10.13 AS builder
COPY ./requirements.txt /home
RUN pip install -r /home/requirements.txt

FROM python:3.10.13-slim-bullseye
EXPOSE 8080
WORKDIR /home
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY ./setup.sh /home
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* /tmp/*
ENTRYPOINT ["/home/setup.sh"]