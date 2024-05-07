import os

kafka_config = {
    'bootstrap.servers': os.environ['KAFKA_BROKER']
}

producer_config = {
    **kafka_config,
    'linger.ms': 0,
}

consumer_config = {
    **kafka_config,
    'group.id': 'crypto-saving-group',
    'auto.offset.reset': 'earliest',
    # автоматически отправляем оффсеты каждые 3 секунды
    'auto.commit.interval.ms': 3000
}

schema_registry_config = {
    'url': os.environ['SCHEMA_REGISTRY_URL']
}