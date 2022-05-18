from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker
from flask import jsonify, request, Blueprint
from flask_bcrypt import Bcrypt
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, get_jwt
from schemas import *
from check import *
from datetime import timezone,datetime
from models import *

query = Blueprint("query", __name__)
b = Bcrypt()


##################
# Rating
##################
@query.route('/rating', methods=['GET'])
@jwt_required()
def get_rating():

    ratings = s.query(Rating).all()
    if not ratings:
        return {"message": "Ratings could not be found."}, 404
    schema = UserSchema()
    return jsonify(schema.dump(ratings, many=True)), 200


@query.route('/rating', methods=['POST'])
@jwt_required()
def add_rating():
    logged_in_user_id = get_jwt_identity()
    data = request.json
    try:
        RatingSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    check_rating = s.query(Rating).filter(Rating.id == request.json.get('id')).first()
    if data['user_creator_id'] != logged_in_user_id:
        return {"message": "Wrong creator"}, 403
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
@jwt_required()
def update_rating(id):
    logged_in_user_id = get_jwt_identity()
    rating_update = s.query(Rating).filter(Rating.id == id).first()
    if rating_update.user_creator_id != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    if rating_update is None:
        return {"message": "Rating with provided id could not be found."}, 404
    params = request.json
    if not params:
        return {"message": "Empty request body."}, 400
    if 'id' in params:
        return {"message": "You can not change id"}, 400
    if params['user_creator_id'] != logged_in_user_id:
        return {"message": "Wrong creator"}, 403
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
@jwt_required()
def delete_rating(id):
    params = request.json
    logged_in_user_id = get_jwt_identity()
    rating_update = s.query(Rating).filter(Rating.id == id).first()
    if rating_update.user_creator_id != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    rating = s.query(Rating).filter_by(id=id).first()
    if not rating:
        return {"message": "Rating could not be found."}, 404

    if params['user_creator_id'] != logged_in_user_id:
        return {"message": "Wrong creator"}, 403
    s.delete(rating)
    s.commit()
    return {"message": "Rating was successfully deleted."}, 200


##################
# Student
##################

@query.route('/student', methods=['GET'])
@jwt_required()
def get_student():

    user = s.query(User).filter(User.id == id).first()
    student = s.query(Student).all()
    if student is None:
        return {"message": "Student could not be found."}, 404
    schema = StudentSchema()
    return jsonify(schema.dump(student, many=True)), 200


@query.route('/student', methods=['POST'])
@jwt_required()
def add_student():
    logged_in_user_id = get_jwt_identity()

    data = request.json
    if not data:
        return {"message": "Empty request body."}, 400
    if data['created'] != logged_in_user_id:
        return{"message": "Wring creator"},403
    try:
        StudentSchema().load(data)
    except ValidationError as err:
        return err.messages, 422
    student_check_id = s.query(Student).filter(Student.id == request.json.get('id')).first()
    if student_check_id is not None:
        return {"message": "Student with this id already exists."}, 406
    new_student = Student(id=data['id'], firstname=data['firstname'], surname=data['surname'],
                          course=data['course'], best_grade=data['best_grade'], created=data['created'])
    s.add(new_student)
    s.commit()
    return {"message": "Student was successfully created."}, 200


@query.route('/student/grade/<int:best_grade>', methods=['GET'])
@jwt_required()
def get_student_by_grade(best_grade):
    studentgrade = s.query(Student).filter(Student.best_grade == best_grade)
    if studentgrade is None:
        return {"message": "Student could not be found."}, 404
    schema = StudentSchema()
    return jsonify(schema.dump(studentgrade, many=True)), 200


@query.route('/student/<int:id>', methods=['GET'])
@jwt_required()
def get_student_by_id(id):


    studentid = s.query(Student).filter(Student.id == id).first()
    if studentid is None:
        return {"message": "Student could not be found."}, 404
    schema = StudentSchema()
    return schema.dump(studentid), 200


@query.route('/student/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    logged_in_user_id = get_jwt_identity()
    student_update = s.query(Student).filter(Student.id == id).first()
    data = request.json
    schema = StudentSchema()
    if data['created'] != logged_in_user_id:
        return{"message": "Wrong creator"},403
    if student_update.created != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    if 'id' in data:
        return {"message": "You can not change id"}, 400
    if not data:
        return {"message": "Empty request body"}, 400
    check_id = s.query(Student).filter(Student.id == id).first()
    if not check_id:
        return {"message": "Student with provided id does not exists"}, 400
    user = s.query(User).filter(User.id == id).first()

    try:
        schema.load(data)
    except ValidationError as err:
        return err.messages, 400
    for key, value in data.items():
        setattr(check_id, key, value)
    s.commit()
    return {"message": "Student was successfully updated. "}, 200


@query.route('/student/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    logged_in_user_id = get_jwt_identity()
    student_update = s.query(Student).filter(Student.id == id).first()
    if student_update.created != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    student = s.query(Student).filter_by(id=id).first()
    if not student:
        return {"message": "Student could not be found."}, 404
    s.delete(student)
    s.commit()
    return {"message": "Student was successfully  deleted."}, 200


##################
# User
##################
@staticmethod
@query.route('/register', methods=['POST'])
def register_user():
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
    # hashed_password = b.generate_password_hash(data['password'])
    # new_user = User(id=data['id'], name=data['name'], surname=data['surname'],
    #                 username=data['username'], password=hashed_password, accessusers=data['accessusers'])
    new_user = User(**data)
    s.add(new_user)
    s.commit()
    token = new_user.get_token()
    return {'access_token': token}

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
User_array = [ 4 , 5]
@auth.verify_password
def verify_password(username, password):
    user = s.query(User).filter(User.username == username).first()
    if b.check_password_hash(user.password, password):
        return (id, 200)
    else:
        return ({"message": "wrong password or id"}, 401)

@staticmethod
@query.route('/login', methods=['POST'])
def login():
    info = request.authorization
    if not info or not info.username or not info.password:
        return {"message": "mised information"} , 401
    password = info.password
    user = s.query(User).filter(User.username == info.username).first()
    token = user.get_token()
    if not user:
        return {"message": "User could not be found."}, 404
    if b.check_password_hash(user.password, password):
        print(User_array)
        return {'access_token': token}
    else:
        print(User_array)
        return {"message": "wrong password or id"}, 401


@query.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    s.add(TokenBlockList(jti=jti, created_at=now))
    s.commit()
    return jsonify(msg="JWT revoked")


@query.route('/user/<int:id>', methods=['PUT'])
#@jwt_required()
def user_update(id):
    logged_in_user_id = 12
    data = request.json
    schema = UserSchema()
    if 'id' in data:
        return {"message": "You can not change id"}, 400
    if not data:
        return {"message": "Empty request body"}, 400
    check_id = s.query(User).filter(User.id == id).first()
    if not check_id:
        return {"message": "User with provided id does not exists"}, 400
    if check_id.id != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    user_check_username = s.query(User).filter(User.username == request.json.get('username')).first()
    if user_check_username is not None:
        return {"message": "User with this username already exists."}, 406
    user = s.query(User).filter(User.id == id).first()
    if user.id != logged_in_user_id:
        return {'message': 'Access denied'}, 403
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
@jwt_required()
def user_delete(id):
    logged_in_user_id = get_jwt_identity()
    user = s.query(User).filter_by(id=id).first()
    if not user:
        return {"message": "User could not be found."}, 404
    if user.id != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    s.delete(user)
    s.commit()
    return {"message": "User was successfully  deleted."}, 200


@query.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    logged_in_user_id = get_jwt_identity()
    user = s.query(User).filter(User.id == user_id).first()
    if not user:
        return {'message': 'Invalid id provided'}, 404
    if user.id != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    serialized = {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "username": user.username,
        "accessusers": user.accessusers
    }
    return jsonify(serialized), 200