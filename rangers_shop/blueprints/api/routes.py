from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required 

# internal import
from rangers_shop.models import Customer, Product, ProdOrder, Order, db, product_schema, products_schema 


api = Blueprint('api', __name__, url_prefix='/api') # every route needs to be preceeded with /api


@api.route('/token', methods=['GET', 'POST'])
def token():
    
    data = request.json # building api requests no () 
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client Id. Try Again.'
        }
    
@api.route('/shop')
@jwt_required()
def get_shop():

    #this is a list of objects
    allprods = Product.query.all()

    #since we cant send a list of objects through api calls we need to change them into dictionaries/jsonify them
    response = products_schema.dump(allprods) #loop through allprods list of objects and change objects into dictionarys
    return jsonify(response)

@api.route('/order/create/<cust_id>', methods=['POST']) #CREATE is usually paired with POST 
@jwt_required()
def create_order(cust_id):
    
    data = request.json 
    
    customer_order = data['order'] # going to be a list of dictionaries of products
    
    customer = Customer.query.filter(Customer.cust_id == cust_id).first() #existing customer
    if not customer:
        customer = Customer(cust_id) # new customer
        db.session.add(customer)
        
    order = Order() #maake an order so will have a unique primary key
    db.session.add(order)
    
    # loop through the customer orders
    for product in customer_order:
        
        # instantiate a prodorder for each product 
        # def __init__(self, prod_id, quantity, price, order_id, cust_id):
        prodorder = ProdOrder(product['prod_id'], product['sets'], product['reps'], order.order_id, cust_id)
        db.session.add(prodorder)
        
        #for each product we add to our order we need to increment our order_total
        order.increment_ordertotal(prodorder.sets)
        
        #for each product we need to decrement the total quantity available
        current_product = Product.query.get(product['prod_id'])
        current_product.decrement_reps(product['reps'])
        
    db.session.commit()
    
    return {
        'status': 200,
        'message': 'New Order was Created'
    }

@api.route('/order/<cust_id>')
@jwt_required()
def get_orders(cust_id):
    
    # grab all prodorders associated with that customer
    prodorder = ProdOrder.query.filter(ProdOrder.cust_id == cust_id).all()
    
    
    data = []
    
    for order in prodorder:
        
        product = Product.query.filter(Product.prod_id == order.prod_id).first()
        
        product_dict = product_schema.dump(product)
        
        #add key value pairs for the quantity and then what order is aassociated with
        product_dict['reps'] = order.reps # this is the quantity the customer ordered
        product_dict['order_id'] = order.order_id # this is order information
        product_dict['id'] = order.prodorder_id # this makes it unique 
        
        data.append(product_dict)
        
    return jsonify(data)

@api.route('/order/update/<order_id>', methods = ['PUT']) #UPDATE is associated with PUT, so not new data but edited existing data 
@jwt_required()
def update_order(order_id):
    
    data = request.json
    new_quantity = int(data['reps'])
    prod_id = data['prod_id']
    
    
    # grab all the right objects in our database, Product, ProdOrder, Order
    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first() # WHERE order_id = order_id and prod_id = prod_id
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)
    
    
    order.decrement_ordertotal(prodorder.sets) # deleting the original price of the product
    
    prodorder.set_reps(product.sets, new_quantity)
    
    order.increment_ordertotal(prodorder.sets) # adding back the new price based on the new quantity 
    
    diff = abs(new_quantity - prodorder.reps)
    
    if prodorder.reps > new_quantity:
        product.increment_reps(diff) # putting some products back
    else:
        product.decrement_reps(diff) # taking some more quantity away

    prodorder.update_reps(new_quantity)

    db.session.commit()

    return {
        'status': 200,
        'messagae': 'Order was Updated Successfully'
    }
    
    return {
        'status': 200,
        'message': 'Order was Updated Successfully'
    }

@api.route('/order/delete/<order_id>', methods = ['DELETE'])
@jwt_required()
def delete_order(order_id):

    data = request.json
    prod_id = data['prod_id']


    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)


    order.decrement_ordertotal(prodorder.reps) #less $ because deleted a product from our order
    product.increment_reps(prodorder.sets) #getting back some total quantity available to sell 

    db.session.delete(prodorder)
    db.session.commit()

    return {
        'status' : 200,
        'message': 'Order was Deleted Successfully'
    }