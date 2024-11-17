# Project Description

### TIMETABLE | REST API - Python, FastAPI
- Python - 3.12.7
- Postgres Database - pgAdmin - 17.0

### Usage (Command and Steps)

1. setup initial project structure
- This command will display a list of all installed Python packages along with their versions
```bash
pip freeze
```
- Run the following command to generate a list of installed packages
```bash
pip freeze > requirements.txt
```
- To install Python libraries listed in a requirements.txt file, you can use the following command
```bash
pip install -r requirements.txt
```
- uninstall all the packages
```bash
pip uninstall -r requirements.txt
```

2. create virtual envioronment (Do this if require)
```bash
python -m venv myenv
```
3. activate the envioronment (Do this if require)
```bash
.\myenv\Scripts\activate
```

4. create database in pgAdmin (check .env file for database name and other config)
```bash
pgAdmin 4 -> PostgresSQL 17 -> Databases -> Create -> Database -> (Your Database Name)
```

5. Initialize Alembic (Make Sure Alembic is on your requirements.txt file)
```bash
alembic init alembic
```
6. Make Changes in env.py file (import settings and schemas Base)
```bash
from app.database import settings
from app.user.user_schema import Base as UserBase
```

7. Setup SqlAlchemy URL in env.py
```bash
config = context.config
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{
        settings.database_hostname}:{settings.database_port}/{settings.database_name}",
)
```

8. Target Metadata (Add All Schemas Base in Metadata if you have multiple Schemas File)
```bash
target_metadata = [UserBase.metadata]
```

9. Run Below Command (This will init the Version Folder in alembic directory)
```bash
alembic upgrade head
```
10. Generate Init Report (Check versions folder in alembic directory)
```bash
alembic revision --autogenerate -m "initial-report"
```

11. Now, Run this Command (This is made all the require changes in database)
```bash
alembic upgrade head
```

12. for starting api
```bash
uvicorn app.main:app --reload
```