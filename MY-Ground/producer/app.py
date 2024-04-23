from flask import Flask, jsonify, request, render_template, url_for
import mysql.connector
import pika
import json


print("Hello111")
app = Flask(__name__)





credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.0.0.2', 5672, '/', credentials))
channel = connection.channel()


channel.exchange_declare(exchange='health', exchange_type='direct')
channel.queue_declare(queue='health_check')
channel.queue_bind(exchange='health', queue='health_check')

channel.exchange_declare(exchange='Item', exchange_type='direct')
channel.queue_declare(queue='item_creation')
channel.queue_bind(exchange='Item', queue='item_creation')

channel.exchange_declare(exchange='Item', exchange_type='direct')
channel.queue_declare(queue='item_deletion')
channel.queue_bind(exchange='Item', queue='item_deletion')

channel.exchange_declare(exchange='read', exchange_type='direct')
channel.queue_declare(queue='read_queue')
channel.queue_bind(exchange='read', queue='read_queue')

channel.exchange_declare(exchange='read_response', exchange_type='direct')
channel.queue_declare(queue='read_queue_response')
channel.queue_bind(exchange='read_response', queue='read_queue_response')


channel.exchange_declare(exchange='Item', exchange_type='direct')
channel.queue_declare(queue='adding_cart')
channel.queue_bind(exchange='Item', queue='adding_cart')

channel.exchange_declare(exchange='Item', exchange_type='direct')
channel.queue_declare(queue='adding_cart_response')
channel.queue_bind(exchange='Item', queue='adding_cart_response')


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/HealthCheck")
def HC():
    return render_template("HC.html")

@app.route("/ItemCreation")
def IC():
    return render_template("IC.html")

@app.route("/StockManagement")
def ID():
    return render_template("SM.html")

@app.route("/view")
def IV():
    return render_template("view_inventory.html")


@app.route("/OrderProcessing")
def OP():
    
    mydb = mysql.connector.connect(
    host="192.0.0.2",
    user="Akshay",
    database="Inventory",
    password="password"
    )
    
    
    cursor = mydb.cursor()

    # Define the SQL query to retrieve item names and their quantities
    query = "SELECT name AS item, COUNT(*) AS quantity FROM items GROUP BY name"

    # Execute the query
    cursor.execute(query)

    # Fetch all the rows from the result
    results = cursor.fetchall()


    # Render the HTML template with the retrieved data
    return render_template('OP.html', items=results)




@app.route("/result",methods=['POST',"GET"])
def result():
    message = "Connection is Alive"
    print("This is ")
    channel.basic_publish(exchange='health', routing_key='health_check', body=message)
    name="Added to Health Check queue. Check if consumer recieved the message!"
    return render_template("HC.html",name = name)

@app.route("/IC",methods=['GET'])
def ItemCreation():
    name = request.args.get("name")
    type = request.args.get("type")
    price = request.args.get("price")
    info = {"name":str(name), "type":str(type), "price":str(price)}
    print(info)
    channel.basic_publish(exchange='Item', routing_key='item_creation', body=json.dumps(info))
    name="Ad"
    return render_template("IC.html",name = name)


@app.route("/ID",methods=['GET'])
def ItemDeletion():
    name = request.args.get("name")
    
    channel.basic_publish(exchange='Item', routing_key='item_deletion', body=str(name))
    name="Ad"
    return render_template("SM.html",name = name)

@app.route('/read_data', methods=['GET'])
def read_data():
    channel.basic_publish(exchange='read', routing_key='read_queue', body="Show records bro")
    method_frame, _, body = channel.basic_get(queue='read_queue_response', auto_ack=True)
    #channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    if method_frame:
        columns = ["ID", "name", "Type","Price"]
        data = json.loads(body)
        return render_template("view_inventory.html", records=data, colnames=columns,)
    
@app.route('/Oper', methods=['GET'])
def Oper():
    name = request.args.get("name")
    quantity = request.args.get("quantity")
    
    mydb = mysql.connector.connect(
    host="192.0.0.2",
    user="Akshay",
    database="Inventory",
    password="password"
    )
    
    cursor = mydb.cursor()

    # Define the SQL query to retrieve item names and their quantities
    query = "SELECT name AS item, COUNT(*) AS quantity FROM items GROUP BY name"

    # Execute the query
    cursor.execute(query)

    # Fetch all the rows from the result
    results = cursor.fetchall()

    
    info = {"name":str(name), "quantity":str(quantity)}
    print(info)
    
    data = []
    for i in results:
        if (name == str(i[0]) and quantity <= str(i[1])):
            #info1 = {"name":str(i[0]), "quantity":str(i[1])}
            channel.basic_publish(exchange='Item', routing_key='adding_cart', body=json.dumps(info))
            method_frame, _, body = channel.basic_get(queue='adding_cart_response', auto_ack=True)
            #channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            if method_frame:
                data = json.loads(body)
                return render_template("OP.html", records=data, items=results)
            
    return render_template("OP.html", records=data, items=results, msg = "Invalid Item or Quantity")
        
        
    




if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port = 5001)
