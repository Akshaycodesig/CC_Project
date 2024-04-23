import pika
import mysql.connector
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.0.0.2', 5672, '/', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='Item', exchange_type='direct')
channel.queue_declare(queue='item_creation')
channel.queue_bind(exchange='Item', queue='item_creation')

mydb = mysql.connector.connect(
    host="192.0.0.2",
    user="Akshay",
    database="Inventory",
    password="password"
)
c = mydb.cursor()



def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Received message for inserting record: {}".format(data))
    #print("Received message for inserting record: {}".format(data))
    # acknowledge that the message has been received
    
    c.execute("INSERT INTO items (name, type, price) VALUES (%s, %s, %s)", (data["name"], data["type"], data["price"]))
    mydb.commit()
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='item_creation', on_message_callback=callback)
channel.start_consuming()