FROM python:3.7.7

RUN echo "Building container..." && \
mkdir app

WORKDIR /app

COPY . ./

RUN apt-get update -y && \
pip install -r ./requirement.txt && \
pip install -e . && \
echo "Build succeed!" 

CMD ["uwsgi", "wsgi.ini"]
