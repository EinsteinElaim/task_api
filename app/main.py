from flask import Flask,jsonify
from flask_restplus import Api,Resource,fields


# objs
app = Flask(__name__)
api = Api(app, version='1.0', title='Task Management API',description='A simple task manager api') #,doc='/docs'


# error handling
# resource not found
@app.errorhandler(404)
def resource_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({"message":"Resource not found"}), 404

# bad request
@app.errorhandler(400)
def bad_request(e):
    # note that we set the 400 status explicitly
    return jsonify({"message":"Check your request body"}), 400

# method not allowes
@app.errorhandler(405)
def bad_request(e):
    # note that we set the 400 status explicitly
    return jsonify({"message":"Check your request body"}), 405


# internal server error
@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 404 status explicitly
    return jsonify({"message":"There was a problem with the server"}), 500



tasks = [
    {
        "id":1,
        "task":"Learn Java",
        "description":"Aim to learn the basics of the java programming language."
    },
    {
        "id":2,
        "task":"Learn Python",
        "description":"Aim to learn the basics of the python programming language."
    },
    {
        "id":3,
        "task":"Learn C++",
        "description":"Aim to learn the basics of the c++ programming language."
    },
]

"""
Response marshalling - provides an easy way to control what data you actually render in your response or
expect as input in the payload. Using the fields module. also format and filter the response .

The decorator marshal_with() is what actually takes your data object and applies field filtering.
The marshalling can work on single objects, dicts, or lists of objects.

An optional envelope keyword argument is specified to wrap the resulting output.
"""

a_task = api.model('Task',{
    "task":fields.String,
    "description":fields.String
})


"""
Namespaces appear to be intended for organizing REST endpoints within a given API, 

Namespaces are optional, and add a bit of additional organisational touch to the API,
mainly, from a documentation point of view.
A namespace allows you to group related Resources under a common root, and is simple to create:

To bring certain Resources under a given namespace, all you need to do, is to replace @api with @ns_conf. 
Notice also that the name of the namespace replaces the name of the resource, 
so endpoints can simply to refer to /, instead of copying the name of the resource time and again
"""

ns_tasks = api.namespace('tasks', description='Task operations')


@ns_tasks.route('/')
class TasksList(Resource):

    # get all the tasks
    @api.marshal_with(a_task,envelope="content")
    def get(self):
        return tasks

    # create a new task
    @api.expect(a_task)
    def post(self):
        new_task = api.payload
        new_task['id'] = len(tasks) + 1
        tasks.append(new_task)
        return api.payload, 201


@ns_tasks.route('/<int:id>')
class Task(Resource):
    # get a task by id
    def get(self, id):
        # user the inbuilt filter() function to get a task that matches the id provided
        task = filter(lambda anDict: anDict['id'] == id, tasks)
        theTask = list(task)
        return theTask[0]

    # delete a task by id
    def delete(self, id):
        tasks.pop(id-1)
        return {"message":"task successfully deleted!"}

    # update a task by id.
    def put(self,id):
        # user the inbuilt filter() function to get a task that matches the id provided
        task = filter(lambda anDict: anDict['id'] == id, tasks)
        theTask = list(task)[0]
        # get the payload
        payload = api.payload
        # perform the updates
        if u'task' in payload:
            theTask['task'] = payload['task']
        if u'description' in payload:
            theTask['description'] = payload['description']

        print(theTask)

        return {"message":"task successfully updated!"}


if __name__ == '__main__':
    app.run()