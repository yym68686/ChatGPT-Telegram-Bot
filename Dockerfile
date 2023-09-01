FROM python:3.10.13
WORKDIR /home
EXPOSE 8080
COPY ./setup.sh /home
COPY ./requirements.txt /home
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/* && pip install -r /home/requirements.txt
ENTRYPOINT ["/home/setup.sh"]