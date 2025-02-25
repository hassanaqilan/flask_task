from flask import Flask, request
from flask.views import MethodView
from Student import Student

students: list = []

app = Flask(__name__)


class StudentAPI(MethodView):
    def get(self, student_id=None):
        if student_id is None:
            return {'students': [student.__dict__ for student in students]}
        else:
            try:
                student = students[student_id]
                return student.__dict__
            except IndexError:
                return {'response': f'{student_id} not found'}, 404

    def post(self):
        try:
            id = students[-1].id + 1 if students else 0
            name = request.json['name']
            age = request.json['age']
            grade = request.json['grade']
            student = Student(id, name, age, grade)
            students.append(student)
            return {
                'response': f'{student.id} has been added'
            }, 201
        except KeyError as e:
            return {'response': f'Missing parameter: {str(e)}'}, 400

    def put(self, student_id):
        try:
            req = request.json
            student = students[student_id]
            student.update(req)
            return student.__dict__
        except (IndexError, KeyError) as e:
            return {'response': f'Error updating student: {str(e)}'}, 400

    def delete(self, student_id):
        try:
            students.pop(student_id)
            return {
                'response': f'{student_id} has been removed'
            }
        except IndexError:
            return {'response': f'{student_id} not found'}, 404


# Register the class-based view with URL rules
student_view = StudentAPI.as_view('student_api')
app.add_url_rule('/student/', view_func=student_view, methods=['POST', 'GET'])
app.add_url_rule(
    '/student/<int:student_id>',
    view_func=student_view,
    methods=['GET', 'PUT', 'DELETE'],
)

if __name__ == '__main__':
    app.run(debug=True)
