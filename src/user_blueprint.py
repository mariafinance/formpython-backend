from flask import Blueprint, request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.user_model import User
import json
from mongoengine.errors import NotUniqueError
from werkzeug.security import check_password_hash

user = Blueprint("user", __name__)


@user.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        User(**data).save()  # unpacking the data and saving it to the database
        return Response(json.dumps({"msg": "User registered"}), status=201)
    except NotUniqueError:
        return Response(json.dumps({"msg": "Email already in use"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@user.route("/check_duplicate_email/<string:email>", methods=["GET"])
def check_duplicate_email(email):
    try:
        if User.objects(email=email):
            return Response(json.dumps({"msg": "Email already in use"}), status=400)
        return Response(json.dumps({"msg": "Email available"}), status=200)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@user.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = User.objects(email=data["email"]).first()
        if user:
            if check_password_hash(user.password, data["password"]):
                fullname = f"{user.givenName}  {user.surName}"
                identity = {"fullname": fullname, "email": user.email}
                access_token = create_access_token(identity=identity)
                return Response(
                    json.dumps(
                        {"msg": "Login successful", "access_token": access_token}
                    ),
                    status=200,
                )
        return Response(json.dumps({"msg": "Invalid credentials"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)
