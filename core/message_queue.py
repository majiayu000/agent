import pika
from typing import Callable, Any
from config.settings import USE_MESSAGE_QUEUE, MESSAGE_QUEUE_CONFIG


class MessageQueue:
    def __init__(self):
        if USE_MESSAGE_QUEUE:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(**MESSAGE_QUEUE_CONFIG)
            )
            self.channel = self.connection.channel()
        else:
            self.connection = None
            self.channel = None

    def publish(self, queue_name: str, message: str) -> None:
        if USE_MESSAGE_QUEUE:
            self.channel.queue_declare(queue=queue_name)
            self.channel.basic_publish(
                exchange="", routing_key=queue_name, body=message
            )

    def consume(
        self, queue_name: str, callback: Callable[[Any, Any, Any, str], None]
    ) -> None:
        if USE_MESSAGE_QUEUE:
            self.channel.queue_declare(queue=queue_name)
            self.channel.basic_consume(
                queue=queue_name, on_message_callback=callback, auto_ack=True
            )
            self.channel.start_consuming()

    def close(self) -> None:
        if self.connection:
            self.connection.close()
