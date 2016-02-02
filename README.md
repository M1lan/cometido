
### Tutorial and explanation at
http://techarena51.com/index.php/buidling-a-database-driven-restful-json-api-in-python-3-with-flask-flask-restful-and-sqlalchemy/

### Steps to Install

     git clone
     pip install -r requirements.txt

     # Edit your config file
     config.py

     #Add  and save your database details
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
