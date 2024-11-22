FROM python:3.13-alpine

RUN apk update
RUN mkdir /modnyk

WORKDIR /modnyk


COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip & pip install -r ./requirements.txt

CMD ["python", "src/manage.py", "runserver", "8008"]