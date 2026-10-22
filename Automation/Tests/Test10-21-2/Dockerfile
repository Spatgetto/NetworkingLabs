FROM python:3.14.4-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV ANSIBLE_HOST_KEY_CHECKING 0

WORKDIR /devops

COPY requirements.txt /devops/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /devops/

CMD ["ansible-playbook", "-i", "hosts", "Test10-21.yml"]
