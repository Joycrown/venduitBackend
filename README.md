
Navigate into the project directory
```bash
cd backend_staging_environment
```

Create a python environment

```bash
python3.10 -m venv stagingBackend
```

Activate the environment

```bash
source stagingBackend/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

Make sure you have postgresql installed and activated, and create a `venduit` database. 

Migrate the database schema with alembic

```bash
(stagingBackend) olyray@MSI:~/backend_staging_environment$ alembic upgrade head
Engine(postgresql://postgres:***@localhost:5432/venduit)
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 8a728c5169e1, creating all tables
```

Then run main.py

```bash
(stagingBackend)~/backend_staging_environment$ python main.py
Engine(postgresql://postgres:***@localhost:5432/venduit)
```
This means that the connection to your local database has been succesful. 

Start the FastAPI application with uvicorn

```bash
(stagingBackend) olyray@MSI:~/backend_staging_environment$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/home/olyray/backend_staging_environment']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [33918] using WatchFiles
Engine(postgresql://postgres:***@localhost:5432/venduit)
INFO:     Started server process [33923]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

