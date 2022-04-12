import pika

from dotenv import load_dotenv
import os

from website.models import Result
from . import db, create_app 


load_dotenv()

connection_url = os.environ.get('connection_url')

app = create_app()

def got_msg(ch, method, properties, body):
    msg = body.decode('utf-8')

    l = msg.split(';')

    with app.app_context():
        new_result = Result(result=l[1], roll=l[0])
        db.session.add(new_result)
        db.session.commit()
        print(" [x] Received %r" % l)
        results = Result.query.filter().all()
        for result in results:
            print(f'{result.roll} - {result.result}')
        print(results)


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
