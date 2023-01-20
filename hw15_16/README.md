### RESTful api
Api performed by using `FastAPI` framework.

#### About
Postgres is used as the database. User are able to do following things:

* Registation user using `POST` method.
* Obtain `JWT` authentication token.
* Operations with articles:
  * obtain all stored articles
  * obtain single article
  * `Only for authenticated:`
    * create new article.
    * edit existing article.
    * delete existing article.

`black` was used to format code

### Visit `/doc` or `/redoc` to see how to operate with this api

## Steps how to start project

1. Python 3.9
2. Install poetry
3. Run `poetry install` in `project_name_directory`
4. In `config` create `.env` file where you need to you need to specify following:
   * DB_URL=`connection url`
   * SECRET_KEY=`your secret_key`
   * ALGORITHM=`algorithm according to jwt-jose`
   * EXPIRE_TOKEN=`expire token time`
5. And finally run `app.py` and visit `/doc` to see further information

## Tests coverage 97%
1. Add to `.env` following row:
    * TEST_DB_URL=`your connection url to test db`
2. Run `pytest tests  --cov` when you are in `api/` folder
