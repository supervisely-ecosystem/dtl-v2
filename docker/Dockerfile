FROM supervisely/base-py-sdk:6.73.74

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y

RUN pip3 install supervisely==6.73.74 jsonschema==4.19.2 networkx==3.1
RUN pip3 install scikit-image==0.21.0 cacheout==0.14.1 markdown==3.5.1
RUN pip3 install json2html==1.3.0 moviepy==1.0.3
RUN pip3 imgaug==0.4.0 imagecorruptions==1.1.2

# COPY dev_requirements.txt dev_requirements.txt
# RUN pip install -r dev_requirements.txt
