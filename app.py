from flask import Flask, request
from Student import Student

students: list = []
students.append(Student(0, 'John', 21, 90))
students.append(Student(1, 'Jane', 22, 95))

app = Flask(__name__)


@app.route('/hello/<name>')
def home(name: str):
    response = {'response': f'Hello, {name}, how is life?'}
    return response


@app.route('/student', methods=['POST'])
def create_student():
    id = students[-1].id + 1
    name = request.json['name']
    age = request.json['age']
    grade = request.json['grade']
    student = Student(id, name, age, grade)
    students[id] = student
    return {'response': f'{student.id} has been added to the list of students'}


@app.route('/students')
def get_students():
    return {'students': [student.__dict__ for student in students]}


@app.route('/student/<int:id>')
def get_student(id: int):
    try:
        student = students[id]
        return student.__dict__
    except IndexError:
        return {'response': f'{id} not found'}


@app.route('/student', methods=['PUT'])
def update_student():

    try:
        req = request.json
        id = req['id']
        student = students[id]
        student.update(req)
        return student.__dict__
    except Exception as e:
        return {'response': e.__str__()}


@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id: int):
    try:
        students.remove(students[id])
        return {'response': f'{id} has been removed from the list of students'}
    except Exception as e:
        return {'response': e.__str__()}


if __name__ == '__main__':
    app.run(debug=True)
