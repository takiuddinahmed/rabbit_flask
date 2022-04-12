from website import create_app
from threading import Thread

app = create_app()
from website.consume import consume_que_msg


if __name__ == "__main__":
    consume_thread = Thread(target=consume_que_msg, daemon=True)
    consume_thread.start()
    app.run(debug=True, port=5555)