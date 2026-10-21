FROM python:3.14.4-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /devops

COPY requirements.txt /devops/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /devops/

CMD ["python", "Test10-21.py"]