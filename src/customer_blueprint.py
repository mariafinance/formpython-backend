from flask import Blueprint, request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.customer_model import Customer
import json
from mongoengine.errors import NotUniqueError


customer = Blueprint("customer", __name__)


@customer.route("/create", methods=["POST"])
def add_customer():
    try:
        data = request.get_json()
        print(data)
        Customer(**data).save()
        return Response(json.dumps({"msg": "Customer added"}), status=201)
    except NotUniqueError:
        return Response(json.dumps({"msg": "Email or AFM already in use"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@customer.route("/email/<string:email>", methods=["GET"])
def get_customer_by_email(email):
    try:
        customer = Customer.objects(email=email).first()
        if customer:
            return Response(json.dumps(customer.to_json()), status=200)
        return Response(json.dumps({"msg": "Customer not found"}), status=404)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@customer.route("/afm/<string:afm>", methods=["GET"])
def get_customer_by_afm(afm):
    try:
        customer = Customer.objects(afm=afm).first()
        if customer:
            return Response(json.dumps(customer.to_json()), status=200)
        return Response(json.dumps({"msg": "Customer not found"}), status=404)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)
