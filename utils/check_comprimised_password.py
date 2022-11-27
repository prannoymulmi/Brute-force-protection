import hashlib

import requests
from pydantic.fields import defaultdict

PAWNED_URL = "https://api.pwnedpasswords.com/range/{}"

"""
This function uses the api provided by pwnedpasswords and uses k-anonymity 
"""
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
    if leaked_passwd_freq.get(hex_digest_remaining):
        return True
    return False
