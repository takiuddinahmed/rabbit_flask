import pika

from dotenv import load_dotenv
import os
from . import db
#from website.models import Result 
load_dotenv()

connection_url = os.environ.get('connection_url')




def got_msg(ch, method, properties, body):
    msg = body.decode('utf-8')
    
    l = msg.split(';')
    '''new_result = Result(result=l[1], roll=l[0])
    db.session.add(new_result)
    db.session.commit()'''
    print(" [x] Received %r" % l)


def consume_que_msg():
    connection = pika.BlockingConnection(pika.URLParameters(connection_url))

    channel = connection.channel()

    channel.queue_declare(queue="message")

    channel.basic_consume(
        queue="message",
        auto_ack=True,
        on_message_callback=got_msg
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()