crypto_price_schema = """{
    "type": "record",
    "name": "CryptoPrice",
    "fields": [
        {"name": "BTCUSD", "type": "float"},
        {"name": "ETHUSD", "type": "float"},
        {"name": "TONUSD", "type": "float"}
    ]
}
"""