FROM python:3.8-slim-buster

WORKDIR /src/webdict

COPY requirements.txt setup.py /src/webdict/
RUN pip install -r /src/webdict/requirements.txt

COPY static/. /src/webdict/static/

COPY webdict/. /src/webdict/webdict/
RUN cd /src/webdict && python setup.py develop

ENV DEBUG False
ENV DJANGO_SETTINGS_MODULE "webdict.djangoapp.app.settings"
CMD python -u webdict/main.py

EXPOSE 8000
STOPSIGNAL SIGINT
