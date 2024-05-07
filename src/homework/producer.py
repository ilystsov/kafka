# producer.py
import logging
import os
from time import sleep

import requests
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.avro import AvroSerializer

from .kafka_utils import producer_config, schema_registry_config
from .kafka_schemas import crypto_price_schema

SEND_PERIOD = 5
POLL_TIMEOUT = 1

producer_logger = None


def setup_logger():
    global producer_logger
    if not producer_logger:
        producer_logger = logging.getLogger(__name__)
        producer_logger.setLevel(logging.INFO)
        handler = logging.FileHandler('producer.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        producer_logger.addHandler(handler)


def delivery_report(err, msg):
    if err is not None:
        producer_logger.error(f'Message delivery failed: {err}')
    else:
        producer_logger.info(f'Message delivered to {msg.topic()} topic, partition number {msg.partition()}')


def fetch_currency():
    try:
        url = os.environ['CRYPTOCOMPARE_URL']
        params = {
            "fsyms": "BTC,ETH,TON",
            "tsyms": "USD"
        }
        response = requests.get(url, params=params)
        data = response.json()
        return data
    except requests.RequestException as e:
        producer_logger.error(f"Failed to fetch currency data: {e}")
        return None


if __name__ == '__main__':
    setup_logger()

    producer = Producer(producer_config)

    schema_registry_client = SchemaRegistryClient(schema_registry_config)
    avro_serializer = AvroSerializer(schema_registry_client, crypto_price_schema)

    while True:
        data = fetch_currency()
        if data:
            record = {
                "BTCUSD": data['BTC']['USD'],
                "ETHUSD": data['ETH']['USD'],
                "TONUSD": data['TON']['USD']
            }
            context = SerializationContext('CryptoPrice', MessageField.VALUE)
            # помещаем сообщения в буфер.
            producer.produce(topic="CryptoPrice", value=avro_serializer(record, context), callback=delivery_report)
            # узнаём у брокера про статус сообщений (отправлены ли из буфера или еще ждут отправки)
            # и в течение 1 секунды ждём ответа. Если для сообщения получен ответ от брокера (подтверждение
            # доставки или сообщение об ошибке), то вызываем колбэк.
            # когда брокер отправит сообщения из буфера? - например, когда пройдет linger.ms или буфер заполнится
            # на batch.size. эти параметры регулируем конфигом.
            producer.poll(timeout=POLL_TIMEOUT)
        sleep(SEND_PERIOD)
