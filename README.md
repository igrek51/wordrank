# Webdict

Web application for vocabulary training with dynamically changing word ranks

## Running

Run on localhost:

```bash
make setup # setup virtualenv and install dependencies
. venv/bin/activate
make run
```

and visit http://127.0.0.1:8000.

You can also run it inside a local docker container:

```bash
make run-docker
```

## Database Management
Visit `/admin` endpoint to access administration panel and manage data models.
In first place, setup your admin account:
```bash
cd backend
python webdict/djangoapp/manage.py createsuperuser
```

## Tech stack

- **Python 3.8**
- **Fastapi** & **Uvicorn** for serving API
- **Django** for managing data models
- **SQLite** for storing data
- **Docker**
- **Angular 6** & **Typescript** for frontend app
- **Bootstrap** for styling theme

## Example screenshots

![](https://github.com/igrek51/webdict-python/blob/master/docs/img/webdict-screen-1.png)

![](https://github.com/igrek51/webdict-python/blob/master/docs/img/webdict-screen-2.png)
