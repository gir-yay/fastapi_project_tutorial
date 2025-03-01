# fastapi_project_tutorial
#### tuturial by kodekloud


pip install fastapi[all]

pip install psycopg2
pip install sqlalchemy 


pip install passlib[bcrypt]

pip install python-jose[cryptography] 


#### Run the app
uvicorn app.main:app --reload



#### killing the processes of the app runing
tasklist /FI "IMAGENAME eq python.exe"
taskkill /PID 24508  /F