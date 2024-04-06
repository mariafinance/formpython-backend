from flask import Blueprint, request, Response
from src.user_model import User
import json
from mongoengine.errors import NotUniqueError

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
