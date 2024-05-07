# test_producer.py
from unittest.mock import patch, Mock

from dotenv import load_dotenv
from requests.exceptions import RequestException
load_dotenv()

from src.homework.producer import fetch_currency


def test_fetch_currency_success():
    expected_data = {
        "BTC": {"USD": 50000},
        "ETH": {"USD": 1500},
        "TON": {"USD": 500}
    }
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: expected_data)
        result = fetch_currency()
        assert result == expected_data


def test_fetch_currency_failure():
    with patch('requests.get', side_effect=RequestException("Unable to connect")), \
            patch('src.homework.producer.producer_logger') as mock_logger:
        result = fetch_currency()
        assert result is None
        mock_logger.error.assert_called_with("Failed to fetch currency data: Unable to connect")

