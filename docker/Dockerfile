FROM supervisely/base-py-sdk:6.73.74

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update

COPY dev_requirements.txt dev_requirements.txt
RUN pip install -r dev_requirements.txt
