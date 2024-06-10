FROM supervisely/base-py-sdk:6.73.74

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y

COPY dev_requirements.txt dev_requirements.txt
RUN pip3 install -r dev_requirements.txt
