FROM python:3.10-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install -y python-pydot python-pydot-ng graphviz
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=index.py
CMD ["flask", "run", "--host", "0.0.0.0"]