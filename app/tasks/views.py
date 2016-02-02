from flask import Blueprint, request, jsonify, make_response
from app.tasks.models import Tasks, TasksSchema, db
from flask_restful import Api, Resource


from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

tasks = Blueprint('tasks', __name__)
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
#https://github.com/marshmallow-code/marshmallow-jsonapi
schema = TasksSchema()
api = Api(tasks)

# Tasks
class TasksList(Resource):
    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""
    def get(self):
        tasks_query = Tasks.query.all()
        results = schema.dump(tasks_query, many=True).data
        return results

    """http://jsonapi.org/format/#crud
    A resource can be created by sending a POST request to a URL that represents a collection of resources. The request MUST include a single resource object as primary data. The resource object MUST contain at least a type member.
    If a POST request did not include a Client-Generated ID and the requested resource has been created successfully, the server MUST return a 201 Created status code"""

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
                schema.validate(raw_dict)
                task_dict = raw_dict['data']['attributes']
                task = Tasks(
                    task_dict['title'],
                    task_dict['description'],
                    task_dict['due_datetime'],
                    task_dict['complexity'],
                    task_dict['urgency'],
                    task_dict['importance'],
                    task_dict['user_id']
                    )
                task.add(task)
                query = Tasks.query.get(task.id)
                results = schema.dump(query).data
                return results, 201

        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 403
                return resp

        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 403
                return resp


class TasksUpdate(Resource):

    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""

    def get(self, id):
        task_query = Tasks.query.get_or_404(id)
        result = schema.dump(task_query).data
        return result

    """http://jsonapi.org/format/#crud-updating
    The PATCH request MUST include a single resource object as primary data. The resource object MUST contain type and id members.
    If a request does not include all of the attributes for a resource, the server MUST interpret the missing attributes as if they were included with their current values. The server MUST NOT interpret missing attributes as null values.
    If a server accepts an update but also changes the resource(s) in ways other than those specified by the request (for example, updating the updated-at attribute or a computed sha), it MUST return a 200 OK response. The response document MUST include a representation of the updated resource(s) as if a GET request was made to the request URL.
    A server MUST return 404 Not Found when processing a request to modify a resource that does not exist."""

    def patch(self, id):
        task = Tasks.query.get_or_404(id)
        raw_dict = request.get_json(force=True)

        try:
            schema.validate(raw_dict)
            task_dict = raw_dict['data']['attributes']
            for key, value in task_dict.items():

                setattr(task, key, value)

            task.update()
            return self.get(id)

        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp

        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp

    #http://jsonapi.org/format/#crud-deleting
    #A server MUST return a 204 No Content status code if a deletion request is successful and no content is returned.
    def delete(self, id):
        task = Tasks.query.get_or_404(id)
        try:
            delete = task.delete(task)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp


api.add_resource(TasksList, '')
api.add_resource(TasksUpdate, '/<int:id>')
