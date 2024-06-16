from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from mongoengine import connect
from src.user_blueprint import user
from src.customer_blueprint import customer_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "super secret and difficult to guess key"

#mongodb+srv://<username>:<password>@cluster0.skyg6ev.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
connect(
    host="mongodb+srv://pyadmin:passwordstring@cluster0.skyg6ev.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    db="Coding-Factory",
    alias="coding-factory",
)
CORS(app)
# cors = CORS(
#     app,
#     resources={r"*": {"origins": ["http://localhost:4200"]}},
# )

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(customer_bp, url_prefix="/customer")
