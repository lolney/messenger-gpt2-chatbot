FROM python:3.7.3-slim-stretch

RUN apt-get -y update && apt-get -y install gcc

ADD . /flask_app
WORKDIR /flask_app
RUN pip3 install -r requirements.txt

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["python3", "-X", "utf8", "app.py"]