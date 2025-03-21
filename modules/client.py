import random
import time

from eth_account import Account
from eth_account.messages import encode_defunct

from modules.config import logger
from modules.http import HttpClient


class Client:
    BASE_URL = "https://app.ether.fi/api/king-claim-chain"

    def __init__(self, _id: str, private_key: str, proxy=None):
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.label = f"{_id} {self.address} | EtherFI |"
        self.http = HttpClient(proxy=proxy)

    def __str__(self) -> str:
        return f"Wallet(address={self.address})"

    def sign_message(self, message: str) -> str:
        message_encoded = encode_defunct(text=message)
        signed_message = self.account.sign_message(message_encoded)

        return "0x" + signed_message.signature.hex()

    def get_preference(self):
        resp = self.http.get(f"{self.BASE_URL}/{self.address}")
        data = resp.json()

        if "chain" in data:
            logger.debug(f"{self.label} KING network preference is set to {data['chain']}")
            return True

        return False

    def set_preference(self, message):
        signature = self.sign_message(message)
        payload = {"address": self.address, "message": message, "signature": signature}

        resp = self.http.post(f"{self.BASE_URL}/{self.address}", json=payload)
        data = resp.json()

        if data.get("success"):
            logger.success(f"{self.label} Success")
            time.sleep(random.randint(3, 7))
            return self.get_preference()
        else:
            logger.error(f"{self.label} {data}")
            return False
