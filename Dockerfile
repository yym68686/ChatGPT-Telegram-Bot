# docker build --no-cache -t chatgpt:1.0 --platform linux/amd64 .
# docker tag chatgpt:1.0 yym68686/chatgpt:1.0
# docker push yym68686/chatgpt:1.0
# FROM python:3.10.13-slim-bullseye
FROM ubuntu:22.04
WORKDIR /home
EXPOSE 8080
COPY ./setup.sh /
RUN apt-get -y update && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt install -y python3.10 python3-pip git python3.10-dev build-essential
# RUN apt-get update \
#     && apt-get install -y software-properties-common \
#     && add-apt-repository ppa:ubuntu-toolchain-r/test && apt-get update \
#     && apt-get install -y git build-essential python3.10-dev \
#     && rm -rf /var/lib/apt/lists/* && pip install --upgrade pip
ENTRYPOINT ["/setup.sh"]