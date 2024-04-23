import pika
import mysql.connector
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.0.0.2', 5672, '/', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='Item', exchange_type='direct')
channel.queue_declare(queue='adding_cart')
channel.queue_bind(exchange='Item', queue='adding_cart')

channel.exchange_declare(exchange='Item', exchange_type='direct')
channel.queue_declare(queue='adding_cart_response')
channel.queue_bind(exchange='Item', queue='adding_cart_response')



mydb = mysql.connector.connect(
    host="192.0.0.2",
    user="Akshay",
    database="Inventory",
    password="password"
)

def callback(ch, method, properties, body):
    mydb = mysql.connector.connect(
    host="192.0.0.2",
    user="Akshay",
    database="Inventory",
    password="password"
    )
    
    
    data = json.loads(body)
    print("Received message for adding to cart: {}".format(data))
    c = mydb.cursor()
    c.execute("INSERT INTO cart (name, quantity) VALUES (%s, %s) ON DUPLICATE KEY UPDATE quantity = %s", (data["name"], data["quantity"], data["quantity"]))
    mydb.commit()
    
    
    c1 = mydb.cursor()
    query = "SELECT name, price FROM items"
    c1.execute(query)
    
    results = c1.fetchall()
    data = {}

    for row in results:
        name = row[0]
        price = row[1]
        data[name] = price
    
    print(data)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    c2 = mydb.cursor()
    query1 = "SELECT * FROM cart"
    c2.execute(query1)
    
    results1 = c2.fetchall()
    print(results1)
    
    Total_price = 0
    for i in results1:
        Total_price = Total_price + (int(data[i[0]]) * int(i[1]))
    
    for i in range(len(results1)):
        results1[i] = results1[i] + (str(int(data[results1[i][0]]) * int(results1[i][1])),)
    
    Cart = results1 + [("price",str(Total_price))]
    
    print (Cart)
    ch.basic_publish(exchange='Item', routing_key='adding_cart_response', body=json.dumps(Cart))
    #ch.basic_ack(delivery_tag=method.delivery_tag)

    

channel.basic_consume(queue='adding_cart', on_message_callback=callback)
print('Waiting for messages.')

channel.start_consuming()


