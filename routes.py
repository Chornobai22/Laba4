from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker
from flask import jsonify, request, Blueprint
from flask_bcrypt import Bcrypt
from check import *
from models import *
from schemas import *
session = sessionmaker(bind=engine)
s = session()
query = Blueprint("query", __name__)

b = Bcrypt()

##################
#Rating
##################

@query.route('/rating', methods=['GET'])
def get_rating():
    rating = s.query(Rating).all()
    if rating is None:
        return {"message": "Ratings could not be found."}, 404
    schema = RatingSchema()
    return jsonify(schema.dump(rating, many=True)), 200

@query.route('/rating', methods=['POST'])
def add_rating():
    data = request.json
    try:
        RatingSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    check_rating = s.query(Rating).filter(Rating.id == request.json.get('id')).first()
    if check_rating is not None and request.json.get('id') != id:
        return {"message": "Rating with provided id already exists"}, 406
    check_user = s.query(User).filter(User.id == request.json.get('user_creator_id')).first()
    if not check_user:
        return {"message": 'User with provided id was not found.'}, 404
    check_accessusers = s.query(User).filter(User.id == request.json.get('user_creator_id')).first()
    if check_accessusers.accessusers != 'Admin':
        return {"message": "This user is not an Admin."}, 406
    student_check_id = s.query(Student).filter(Student.id == request.json.get('Student_id')).first()
    if not student_check_id:
        return {"message": "Student with this id was not found."}, 404
    schema = RatingSchema()
    s.add(schema.load(data))
    s.commit()
    return {"message": "New Rating was successfully created. "}, 200

@query.route('/rating/<int:id>', methods=['PUT'])
def update_rating(id):
    rating_update = s.query(Rating).filter(Rating.id == id).first()
    if rating_update is None:
        return {"message": "Rating with provided id could not be found."}, 404
    params = request.json
    if not params:
        return {"message": "Empty request body."}, 400
    if 'id' in params:
        return {"message": "You can not change id"}, 400
    schema = RatingSchema()
    try:
        data = schema.load(params)
    except ValidationError as err:
        return err.messages, 422
    student_check_id = s.query(Student).filter(Student.id == request.json.get('Student_id')).first()
    if not student_check_id:
        return {"message": "Student with this id was not found."}, 404
    check_user = s.query(User).filter(User.id == request.json.get('user_creator_id')).first()
    if not check_user:
        return {"message": 'User with provided id was not found.'}, 404
    check_accessusers = s.query(User).filter(User.id == request.json.get('user_creator_id')).first()
    if check_accessusers.accessusers != 'Admin':
        return {"message": "This user is not an Admin."}, 406
    for key, value in params.items():
        setattr(rating_update, key, value)
    s.commit()
    return {"message": "Rating was successfully updated. "}, 200


@query.route('/rating/<int:id>', methods=['DELETE'])
def delete_rating(id):
    rating = s.query(Rating).filter_by (id=id).first()
    if not rating:
        return {"message": "Rating could not be found."}, 404
    s.delete(rating)
    s.commit()
    return {"message": "Rating was successfully deleted."}, 200

##################
#Student
##################

@query.route('/student', methods=['GET'])
def get_student():
    student = s.query(Student).all()
    if student is None:
        return {"message": "Student could not be found."}, 404
    schema = StudentSchema()
    return jsonify(schema.dump(student, many=True)), 200

@query.route('/student', methods=['POST'])
def add_student():
    data = request.json
    if not data:
        return {"message": "Empty request body."}, 400
    try:
        StudentSchema().load(data)
    except ValidationError as err:
        return err.messages, 422
    student_check_id = s.query(Student).filter(Student.id == request.json.get('id')).first()
    if student_check_id is not None:
        return {"message": "Student with this id already exists."}, 406
    new_student = Student(id=data['id'], firstname=data['firstname'], surname=data['surname'],
                    course=data['course'], best_grade=data['best_grade'])
    s.add(new_student)
    s.commit()
    return {"message": "Student was successfully created."}, 200

@query.route('/student/grade/<int:best_grade>', methods=['GET'])
def get_student_by_grade (best_grade):
    studentgrade = s.query(Student).filter(Student.best_grade == best_grade)
    if studentgrade is None:
        return {"message": "Student could not be found."}, 404
    schema = StudentSchema()
    return jsonify(schema.dump(studentgrade, many=True)), 200

@query.route('/student/<int:id>', methods=['GET'])
def get_student_by_id(id):
    studentid = s.query(Student).filter(Student.id == id).first()
    if studentid is None:
        return {"message": "Student could not be found."}, 404
    schema = StudentSchema()
    return schema.dump(studentid), 200

@query.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json
    schema = StudentSchema()
    if 'id' in data:
        return {"message": "You can not change id"}, 400
    if not data:
        return {"message": "Empty request body"}, 400
    check_id = s.query(Student).filter(Student.id == id).first()
    if not check_id:
        return {"message": "Student with provided id does not exists"}, 400
    try:
        schema.load(data)
    except ValidationError as err:
        return err.messages, 400
    for key, value in data.items():
        setattr(check_id, key, value)
    s.commit()
    return {"message": "Student was successfully updated. "}, 200

@query.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = s.query(Student).filter_by (id=id).first()
    if not student:
        return {"message": "Student could not be found."}, 404
    s.delete(student)
    s.commit()
    return {"message": "Student was successfully  deleted."}, 200

##################
#User
##################

@query.route('/user', methods=['POST'])
def add_user():
    data = request.json
    if not data:
        return {"message": "Empty request body."}, 400
    if 'accessusers' not in data:
        return {"message": "You should set a correct property."}, 400
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return err.messages, 422
    user_check_id = s.query(User).filter(User.id == request.json.get('id')).first()
    if user_check_id is not None:
        return {"message": "User with this id already exists."}, 406
    user_check_username = s.query(User).filter(User.username == request.json.get('username')).first()
    if user_check_username is not None:
        return {"message": "User with this username already exists."}, 406
    hashed_password = b.generate_password_hash(data['password'])
    new_user = User(id=data['id'], name=data['name'], surname=data['surname'],
                    username=data['username'], password=hashed_password, accessusers=data['accessusers'])
    s.add(new_user)
    s.commit()
    return {"message": "User was successfully created."}, 200

@query.route('/user/<int:id>', methods=['PUT'])
def user_update(id):
    data = request.json
    schema = UserSchema()
    if 'id' in data:
        return {"message": "You can not change id"}, 400
    if not data:
        return {"message": "Empty request body"}, 400
    check_id = s.query(User).filter(User.id == id).first()
    if not check_id:
        return {"message": "User with provided id does not exists"}, 400
    user_check_username = s.query(User).filter(User.username == request.json.get('username')).first()
    if user_check_username is not None:
        return {"message": "User with this username already exists."}, 406
    try:
        schema.load(data)
    except ValidationError as err:
        return err.messages, 400
    for key, value in data.items():
        if key == 'password':
            value = Bcrypt().generate_password_hash(value).decode('utf - 8')
        setattr(check_id, key, value)
    s.commit()
    return {"message": "User was successfully updated. "}, 200


@query.route('/user/<int:id>', methods=['DELETE'])
def user_delete(id):
    user = s.query(User).filter_by (id=id).first()
    if not user:
        return {"message": "User could not be found."}, 404
    s.delete(user)
    s.commit()
    return {"message": "User was successfully  deleted."}, 200

@query.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = s.query(User).filter(User.id == id).first()
    if user is None:
        return {"message": "User could not be found."}, 404
    schema = UserSchema()
    return schema.dump(user), 200

