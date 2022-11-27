import hashlib

import requests
from pydantic.fields import defaultdict


PAWNED_URL = "https://api.pwnedpasswords.com/range/{}"

class PasswordCheck:
    """
    This function uses the api provided by pwnedpasswords to check if the password has been already breached.
    The API uses K-Anonymity to accept the SHA1 password. Where only the first 5 letters of the
    SHA1 encoded password is encoded. Then the API returns a range of breached password and the number of times.
    See <a href=https://sanatinia.medium.com/securely-check-if-a-password-is-compromised-in-python-be74bf52b0cc />
    """
    @staticmethod
    def check_compromised_password(passwd: str):
        sha1 = hashlib.sha1()
        sha1.update(passwd.encode())
        hex_digest = sha1.hexdigest().upper()
        # get the first five SHA1 hex
        hex_digest_f5 = hex_digest[:5]
        # The remaining hex
        hex_digest_remaining = hex_digest[5:]
        r = requests.get(PAWNED_URL.format(hex_digest_f5))
        leaked_passwd_freq = defaultdict(int)
        for passwd_freq in r.content.splitlines():
            pass_parts = passwd_freq.split(b":")
            passwd = pass_parts[0].decode()
            freq = pass_parts[1]
            leaked_passwd_freq[passwd] = int(freq)
        return hex_digest_remaining in leaked_passwd_freq


def decoy_function_for_test(passwd: str):
    PasswordCheck.check_compromised_password(passwd)
