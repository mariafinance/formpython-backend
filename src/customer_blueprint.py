from bson import ObjectId
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
#Import the CustomerService
from src.customer_service import CustomerService
from src.customer_model import Address, Customer, PhoneNumber
import json
from mongoengine.errors import NotUniqueError


customer_bp = Blueprint("customer", __name__)
#Use the customer_service.py
customer_service = CustomerService()


@customer_bp.route("/create", methods=["POST"])
def add_customer():
    try:
        data = request.get_json()
        customer_service.create_customer(data)
        print(data)
        #Customer(**data).save()
        return Response(json.dumps({"msg": "Customer added"}), status=201)
    except NotUniqueError:
        return Response(json.dumps({"msg": "Email or AFM already in use"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@customer_bp.route("/email/<string:email>", methods=["GET"])
def get_customer_by_email(email):
    try:
        customer = Customer.objects(email=email).first()
        if customer:
            return Response(json.dumps(customer.to_json()), status=200)
        return Response(json.dumps({"msg": "Customer not found"}), status=404)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@customer_bp.route("/afm/<string:afm>", methods=["GET"])
def get_customer_by_afm(afm):
    try:
        customer = Customer.objects(afm=afm).first()
        if customer:
            return Response(json.dumps(customer.to_json()), status=200)
        return Response(json.dumps({"msg": "Customer not found"}), status=404)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)

@customer_bp.route("/<string:id>", methods=["GET", "PUT", "DELETE"])
def customer_route(id):
    try:
        if request.method == "GET":
            customer = Customer.objects(id=ObjectId(id)).first()
            if customer:
                return Response(json.dumps(customer.to_json()), status=200)
            return Response(json.dumps({"msg": "Customer not found"}), status=404)
        elif request.method == "PUT":
            try:
                data = request.get_json()
                customer = Customer.objects(id=ObjectId(id)).first()
                if customer:
                    # Update simple fields directly
                    customer.givenName = data.get('givenName', customer.givenName)
                    customer.surName = data.get('surName', customer.surName)
                    customer.email = data.get('email', customer.email)
                    customer.afm = data.get('afm', customer.afm)
                    
                    # Update phoneNumbers if provided
                    if 'phoneNumbers' in data:
                        customer.phoneNumbers = [
                            PhoneNumber(number=phone.get('number'), type=phone.get('type'))
                            for phone in data['phoneNumbers']
                        ]
                    
                    # Update address if provided
                    if 'address' in data:
                        customer.address = Address(
                            street=data['address'].get('street', ''),
                            city=data['address'].get('city', ''),
                            number=data['address'].get('number', ''),
                            zipCode=data['address'].get('zipCode', '')
                        )

                    customer.save()  # Save the updated customer document
                    return jsonify({"msg": "Customer updated successfully"}), 200
                
                return jsonify({"msg": "Customer not found"}), 404
            
            except Exception as e:
                print(f"Error updating customer: {e}")
                return jsonify({"msg": "Server error"}), 500
        elif request.method == "DELETE":
            customer = Customer.objects(id=ObjectId(id)).first()
            if customer:
                customer.delete()
                return Response(json.dumps({"msg": "Customer deleted successfully"}), status=200, mimetype='application/json')
            return Response(json.dumps({"msg": "Customer not found"}), status=404, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": "Invalid ID format"}), status=400)

@customer_bp.route("/search", methods=["GET"])
def search_customers():
    afm = request.args.get('afm')
    email = request.args.get('email')
    id = request.args.get('id')

    query = {}
    if afm:
        query['afm'] = afm
    if email:
        query['email'] = email
    if id:
        try:
            query['_id'] = ObjectId(id)
        except:
            return Response(json.dumps({"msg": "Invalid ID format"}), status=400)

    results = Customer.objects(__raw__=query)

    # Convert ObjectId to string for JSON serialization
    customers_list = []
    for customer in results:
        customer_dict = json.loads(customer.to_json())
        customer_dict['_id'] = str(customer.id)
        customers_list.append(customer_dict)

    return jsonify(customers_list)