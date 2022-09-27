FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 6800

ENTRYPOINT [ "/app/scripts/scrapydaemon.sh" ]
CMD [ "bash" ]