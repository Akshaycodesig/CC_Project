import pika
import mysql.connector
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.0.0.2', 5672, '/', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='Item', exchange_type='direct')
channel.queue_declare(queue='item_deletion')
channel.queue_bind(exchange='Item', queue='item_deletion')

mydb = mysql.connector.connect(
    host="192.0.0.2",
    user="Akshay",
    database="Inventory",
    password="password"
)
c = mydb.cursor()

def callback(ch, method, properties, body):
    print("Received message for deleting record: {}".format(body))
    name = body.decode()
    # delete the record from the database
    c.execute("DELETE FROM items WHERE name = %s LIMIT 1", (name,))

    mydb.commit()
    ch.basic_ack(delivery_tag=method.delivery_tag)



channel.basic_consume(queue='item_deletion', on_message_callback=callback)
channel.start_consuming()