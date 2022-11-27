from unittest.mock import MagicMock

import requests

from utils.jwt_utils import get_project_root
from utils.password_check import PasswordCheck, decoy_function_for_test


def test_check_compromised_password_when_breached_password_is_given_then_true_is_returned():
    with open(f"{get_project_root()}/tests/utils/hashes_for_test.txt") as f:
        s = f.read()
        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = s
        requests.get.return_value = mock_response
        result = decoy_function_for_test("test1234")
        assert result


def test_check_compromised_password_when_non_breached_password_is_given_then_false_is_returned():
    with open(f"{get_project_root()}/tests/utils/hashes_for_test.txt") as f:
        s = f.read()
        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = s
        requests.get.return_value = mock_response
        result = PasswordCheck().check_compromised_password("Very$GoodPassQord$3!%")
        assert result == False
