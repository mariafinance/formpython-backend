from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.user_service import UserService
from src.user_model import User, has_role
import json
from mongoengine.errors import NotUniqueError
from werkzeug.security import check_password_hash
from flasgger.utils import swag_from


user = Blueprint("user", __name__)
user_service = UserService()

@user.route("/register", methods=["POST"])
@swag_from({
    'responses': {
        201: {
            'description': 'User registered successfully'
        },
        400: {
            'description': 'Email already in use or other error'
        }
    }
})
def register():
    try:
        data = request.get_json()
        user_service.register_user(data)
        # User(**data).save()  # Uncomment if you are using MongoDB and want to save the user directly
        return Response(json.dumps({"msg": "User is successfully registered"}), status=201)
    except NotUniqueError:
        return Response(json.dumps({"msg": "Email already in use"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)

@user.route("/check_duplicate_email/<string:email>", methods=["GET"])
@swag_from({
    'parameters': [
        {
            'name': 'email',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Email address to check for duplication'
        }
    ],
    'responses': {
        200: {
            'description': 'Email is available'
        },
        400: {
            'description': 'Email already in use or other error'
        }
    }
})
def check_duplicate_email(email):
    try:
        if user_service.check_duplicate_email(email):
            return Response(json.dumps({"msg": "Email already in use"}), status=400)
        return Response(json.dumps({"msg": "Email available"}), status=200)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


# @user.route("/login", methods=["POST"])
# def login():
#     try:
#         data = request.get_json()        
#         #Authenticate user and fetch user details
#         identity = user_service.authenticate_user(data["email"], data["password"])
#         if identity:
#             access_token = create_access_token(identity=identity)
#             user = User.objects(email=data["email"]).first()

#             return Response(
#                     json.dumps(
#                         {"msg": "Login successful",
#                           "access_token":access_token,
#                            "email": user.email
#                           },
#                     ),
#                     status=200,
#                 )
#         return Response(json.dumps({"msg": "Invalid credentials, Try again with correct username and password"}), status=400)
#     except Exception as e:
#         print(e)
#         return Response(json.dumps({"msg": str(e)}), status=400)
@user.route("/login", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'properties': {
                    'email': {
                        'type': 'string',
                        'description': 'User email',
                        'example': 'user@example.com'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'User password',
                        'example': 'password123'
                    }
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Login successful'
                    },
                    'access_token': {
                        'type': 'string',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    },
                    'email': {
                        'type': 'string',
                        'example': 'user@example.com'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid credentials or other error',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Invalid credentials, Try again with correct username and password'
                    }
                }
            }
        }
    }
})
def login():
    try:
        data = request.get_json()
        # Authenticate user and fetch user details
        identity = user_service.authenticate_user(data["email"], data["password"])
        if identity:
            access_token = create_access_token(identity=identity)
            user = User.objects(email=data["email"]).first()

            return Response(
                    json.dumps(
                        {"msg": "Login successful",
                         "access_token": access_token,
                         "email": user.email
                         },
                    ),
                    status=200,
                )
        return Response(json.dumps({"msg": "Invalid credentials, Try again with correct username and password"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)

@user.route('/admin', methods=['GET'])
@jwt_required()
@swag_from({
    'security': [{'jwt': []}],
    'responses': {
        200: {
            'description': 'Welcome admin',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Welcome admin'
                    }
                }
            }
        },
        403: {
            'description': 'Access denied',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Access denied'
                    }
                }
            }
        }
    }
})
def admin():
    current_user = get_jwt_identity()
    user = User.objects(email=current_user['email']).first()
    if not has_role(user, 'admin'):
        return jsonify({"msg": "Access denied"}), 403
    return jsonify({"msg": "Welcome admin"}), 200

@user.route('/protected', methods=['GET'])
@jwt_required()
@swag_from({
    'security': [{'jwt': []}],
    'responses': {
        200: {
            'description': 'Returns the current user identity',
            'schema': {
                'type': 'object',
                'properties': {
                    'logged_in_as': {
                        'type': 'object',
                        'description': 'The user identity',
                        'example': {
                            'email': 'user@example.com',
                            'role': 'user'
                        }
                    }
                }
            }
        }
    }
})
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
