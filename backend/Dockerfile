FROM python:3.8-slim-buster

WORKDIR /src/webict

COPY requirements.txt setup.py /src/webdict/
RUN pip install -r /src/webdict/requirements.txt

COPY webdict/. /src/webdict/webdict/

RUN cd /src/webdict && python setup.py develop

ENV DEBUG False
ENV DJANGO_SETTINGS_MODULE "webdict.djangoapp.app.settings"
ENTRYPOINT ["python", "-u", "manage.py", "runserver"]
CMD ["--settings=django_chords.settings_prod", "--insecure", "0.0.0.0:8000", "--noreload"]

EXPOSE 8000
STOPSIGNAL SIGINT
