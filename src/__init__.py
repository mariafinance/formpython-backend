from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from mongoengine import connect
from src.user_blueprint import user
from src.customer_blueprint import customer_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flasgger import Swagger
from flask_restx import Api
from werkzeug.utils import cached_property

app = Flask(__name__,static_url_path='/static')

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "super secret and difficult to guess key"

#MongoDB Connection
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

# # Initialize Flask-RESTPlus API
# from flask_restplus import Api
# api = Api(app, version='1.0', title='Customer API',
#           description='API endpoints for managing customers')

# # Initialize Flasgger for Swagger UI
# swagger = Swagger(app, template_file='swagger.yaml', url_prefix='/apidocs')

swagger = Swagger(app)

api = Api(app, doc='/apidocs')

# Register Blueprints
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(customer_bp, url_prefix="/customer")
