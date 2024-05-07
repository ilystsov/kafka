# test_consumer.py
from unittest.mock import patch

from dotenv import load_dotenv

load_dotenv()

from src.homework.consumer import save_message


@patch('src.homework.consumer.insert_currency')
def test_save_message_success(mock_insert):
    message = {'BTCUSD': 50000, 'ETHUSD': 1500, 'TONUSD': 500}
    with patch('src.homework.consumer.consumer_logger') as mock_logger:
        save_message(message)
        mock_logger.info.assert_called_with(f"Received record: {message}")

