import pika
import mysql.connector
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.0.0.2', 5672, '/', credentials))

channel = connection.channel()
channel.exchange_declare(exchange='health', exchange_type='direct')
channel.queue_declare(queue='health_check')
channel.queue_bind(exchange='health', queue='health_check')



def callback(ch, method, properties, body):
    data = body.decode()
    print("Message received: {}".format(data))
    # acknowledge that the message has been received
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='health_check', on_message_callback=callback)
channel.start_consuming()