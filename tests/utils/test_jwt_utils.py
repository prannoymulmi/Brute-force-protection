import datetime
from datetime import timezone, timedelta
from unittest.mock import ANY, MagicMock
from unittest.mock import Mock

from jwt.utils import get_int_from_datetime

from schemas.TokenMessage import TokenMessage
from utils.jwt_utils import encode_jwt, decode_jwt, instance


def test_encode_jwt_when_called_a_jwt_token_of_expiry_30_minutes_is_returned(monkeypatch):
    message = TokenMessage(iss="asmis", sub="", iat=get_int_from_datetime(datetime.datetime.now(timezone.utc)),
                           exp=get_int_from_datetime(
                               datetime.datetime.now(timezone.utc) + timedelta(minutes=30)))

    instance.encode = Mock()
    encode_jwt()
    instance.encode.assert_called_with(message.dict(), ANY, alg='RS256')

def test_decode_jwt_then_return_this():
    # instance.encode = Mock()
    # instance.encode.configure_mock(return_value="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiAiYXNtaXMiLCAic3ViIjogIiIsICJpYXQiOiAxNjY4NzgxMzE5LCAiZXhwIjogNDgyMjM4MTMxOX0.edjsqikVLmOqzA_xt5phURKy9KkpCCEStziOUn7mvW7uJzRqpPX_74svoIaOqsKZuSd4evfGoyKRwkafUiKAsGwgRqrxbrfprtCVVUes1lgyD2DWq97f1Xyuwk1LSQrVrvhgmgwlJBj7py-xn03zyjSU8rnueRzadiqzNsEavdSDqGOmIfn1x4WmdKOny7tUSUxtTNyEBYq89wcDQcK2aUFSTyQXS7NZtc0hHK2P4jRj6mHu6qawQg8HpjByvZ5vkRyEr-M08O6Ro_-bMc52IRiXXEiyZuSZFJq6TxjXWwNkAHmNi_gtRhnQL295GaKE35MXVVatCxVWRYBdvH0tfw")
    res = decode_jwt(encode_jwt())
    assert res is not None

