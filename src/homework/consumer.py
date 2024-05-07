# consumer.py
import logging

from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

from confluent_kafka.serialization import SerializationContext, MessageField

from .kafka_utils import schema_registry_config, consumer_config
from .kafka_schemas import crypto_price_schema
from .exceptions import SaveException
from .db import insert_currency

POLL_TIMEOUT = 1.0

consumer_logger = None


def setup_logger():
    global consumer_logger
    if not consumer_logger:
        consumer_logger = logging.getLogger(__name__)
        consumer_logger.setLevel(logging.INFO)
        handler = logging.FileHandler('consumer.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        consumer_logger.addHandler(handler)


def save_message(message: dict) -> None:
    consumer_logger.info(f"Received record: {message}")
    try:
        for currency in message:
            insert_currency(currency, message[currency])
    except SaveException as e:
        consumer_logger.error(f"Error saving message {message}: {e}")


def main():
    setup_logger()
    schema_registry_client = SchemaRegistryClient(schema_registry_config)
    avro_deserializer = AvroDeserializer(schema_registry_client, crypto_price_schema)
    consumer = Consumer(consumer_config)
    consumer.subscribe(['CryptoPrice'])

    try:
        while True:
            msg = consumer.poll(timeout=POLL_TIMEOUT)
            if msg is None:
                continue
            if msg.error():
                consumer_logger.error("Consumer error: {}".format(msg.error()))
                continue

            deserialized_message = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            save_message(deserialized_message)
    finally:
        consumer.close()


if __name__ == '__main__':
    main()
