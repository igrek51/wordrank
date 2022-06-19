FROM python:3.8-slim-buster

WORKDIR /src/wordrank

COPY requirements.txt setup.py /src/wordrank/
RUN pip install -r /src/wordrank/requirements.txt

COPY static/. /src/wordrank/static/

COPY wordrank/. /src/wordrank/wordrank/
RUN cd /src/wordrank && python setup.py develop

ENV DEBUG false
ENV DJANGO_SETTINGS_MODULE "wordrank.djangoapp.app.settings"
CMD python -u wordrank/main.py

EXPOSE 8000
STOPSIGNAL SIGTERM
