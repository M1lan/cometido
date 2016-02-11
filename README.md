
### Tutorial and explanation at
http://techarena51.com/index.php/buidling-a-database-driven-restful-json-api-in-python-3-with-flask-flask-restful-and-sqlalchemy/

### Steps to Install

     git clone

     # Create your python virtual environment
     mkvirtualenv smarttask
     workon smarttask

     pip install -r requirements.txt

     # Make the setup for the DB executable
     chmod +x setup.sh

     # Create a fresh User, and DB in postgres
     ./setup.sh

     # Add in the first three lines the credentials which you have typed in before
     edit config.py

     # Now you have a empty DB which the "smarttask db_manage can access"
     python db_manage.py db init
     python db_manage.py db migrate
     python db_manage.py db upgrade
     python run.py

### Resource URL’s

## users
- GET	`http://localhost:5000/api/v1/users`	Returns a list of all users
- POST	`http://localhost:5000/api/v1/users`	Creates a user and returns with user id
- GET	`http://localhost:5000/api/v1/users/\<user_id\>`	Returns user details for the given user id if the it exists

## tasks
- GET `http://localhost:5000/api/v1/tasks`
- POST	`http://localhost:5000/api/v1/tasks`	Creates a task and returns with task id
- GET	`http://localhost:5000/api/v1/tasks/\<task_id>``	Creates a user and returns with task id
