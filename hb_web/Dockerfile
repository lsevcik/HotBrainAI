FROM fedora:latest

RUN dnf install -y python python-pip

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python", "./app.py"]