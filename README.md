# WordRank

Web application for vocabulary training with dynamic word ranks.

Your goal is to translate the words. 
The more mistakes you make, the higher rank the word gets.
So you'll memorize it better, once it appears more often.

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
python wordrank/djangoapp/manage.py createsuperuser
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

![](./docs/img/screen-1.png)

![](./docs/img/screen-2.png)
