from flask import Blueprint, request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.user_service import UserService
from src.user_model import User
import json
from mongoengine.errors import NotUniqueError
from werkzeug.security import check_password_hash

user = Blueprint("user", __name__)
user_service = UserService()


@user.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        user_service.register_user(data)
        #User(**data).save()  # unpacking the data and saving it to the database
        return Response(json.dumps({"msg": "User is successfully registered"}), status=201)
    except NotUniqueError:
        return Response(json.dumps({"msg": "Email already in use"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@user.route("/check_duplicate_email/<string:email>", methods=["GET"])
def check_duplicate_email(email):
    try:
        if user_service.check_duplicate_email(email):
            return Response(json.dumps({"msg": "Email already in use"}), status=400)
        return Response(json.dumps({"msg": "Email available"}), status=200)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@user.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()        
        #Authenticate user and fetch user details
        identity = user_service.authenticate_user(data["email"], data["password"])
        if identity:
            access_token = create_access_token(identity=identity)
            return Response(
                    json.dumps(
                        {"msg": "Login successful",
                          "access_token": access_token},
                    ),
                    status=200,
                )
        return Response(json.dumps({"msg": "Invalid credentials, Try again with correct username and password"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)
