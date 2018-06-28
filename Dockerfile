FROM ubuntu:latest

ADD pynsxv/ /opt/pynsxv/
ADD pyvmomi/ /opt/pyvmomi/

# install base python packages and PyNSXv
RUN \
  apt-get update && \
  apt-get upgrade -y && \
  apt-get install libssl-dev libffi-dev libxml2-dev libxslt-dev python-dev zlib1g-dev python-pip -y && \
  pip install pyvmomi tabulate nsxramlclient

