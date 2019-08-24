FROM python:3.7.2

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
ENV HOME=/usr/src/app
WORKDIR $HOME

ADD . $HOME
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
CMD python manage.py runserver 0.0.0.0:$PORT         