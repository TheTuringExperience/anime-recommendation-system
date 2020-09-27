FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /api
WORKDIR /api
RUN pip3 install -r requirements.txt
ENTRYPOINT ["uvicorn"]
CMD ["main:api", "--reload", "--host", "0.0.0.0"]
