import pika, sys, os
import datetime
from flask import Flask


app = Flask(__name__)

@app.route("/")
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='RegisterQueue')

    def callback(ch, method, properties, body):
        now= datetime.datetime.now()
        print(" [x] Received and saved at",now, "%r" % body)

    channel.basic_consume(queue='RegisterQueue', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    app.run()