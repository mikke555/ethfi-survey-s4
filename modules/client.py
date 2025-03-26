import random
import time

from eth_account import Account
from eth_account.messages import encode_defunct

from modules.config import logger
from modules.http import HttpClient


class Client:
    KING_PRICE = 711.71
    BASE_URL = "https://app.ether.fi/api"

    def __init__(self, _id: str, private_key: str, proxy=None):
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.label = f"{_id} {self.address} | EtherFI |"
        self.http = HttpClient(self.BASE_URL, proxy)

    def __str__(self) -> str:
        return f"Wallet(address={self.address})"

    def sign_message(self, message: str) -> str:
        message_encoded = encode_defunct(text=message)
        signed_message = self.account.sign_message(message_encoded)

        return "0x" + signed_message.signature.hex()

    def get_allocation(self) -> None:
        resp = self.http.get(f"/king/{self.address}")
        data = resp.json()

        if resp.status_code == 200 and "Amount" in data:
            human_amount = int(data["Amount"]) / 10**18
            amount_usd = human_amount * self.KING_PRICE
            logger.debug(f"{self.label} Your restaking rewards: {human_amount:.6f} KING (${amount_usd:.2f})")
        elif resp.status_code == 500 and "error" in data:
            logger.warning(f"{self.label} This wallet has no restaking rewards")
        else:
            logger.warning(f"{self.label} <{resp.status_code}> {resp.text}")

    def get_preference(self) -> bool:
        resp = self.http.get(f"/king-claim-chain/{self.address}")
        data = resp.json()

        if "chain" in data:
            logger.debug(f"{self.label} KING network preference is set to {data['chain']}")
            self.get_allocation()
            return True

        return False

    def set_preference(self, message: str) -> bool:
        signature = self.sign_message(message)
        payload = {"address": self.address, "message": message, "signature": signature}

        resp = self.http.post(f"/king-claim-chain/{self.address}", json=payload)
        data = resp.json()

        if "success" in data:
            logger.success(f"{self.label} Success")
            time.sleep(random.randint(3, 7))
            return self.get_preference()
        else:
            logger.error(f"{self.label} {data}")
            return False
