# fastapi_project_tutorial
#### tuturial by kodekloud


pip install fastapi[all]

pip install psycopg2
pip install sqlalchemy 


pip install passlib[bcrypt]

pip install python-jose[cryptography] 

pip install alembic
#### using alembic
alembic init alembec
alembic revision -m " sth like a commit msg here to describe what u did in the revision"
alembic revision --autogenerate -m "an auto-generated revision"
alembic upgrade head

##### to downgrade
alembic downgrade -1

##### checking the current version
alembic current

##### checking the history
alembic history

#### Run the app
uvicorn app.main:app --reload



#### killing the processes of the app runing
tasklist /FI "IMAGENAME eq python.exe"
taskkill /PID 24508  /F