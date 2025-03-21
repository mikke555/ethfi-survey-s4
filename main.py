import random
import time
from datetime import datetime

from tqdm import tqdm

from modules.client import Client
from modules.config import logger

CHOICE = "swell"  # ethereum | swell | arbitrum | base
USE_PROXY = True
SHUFFLE_KEYS = False
SLEEP_BETWEEN_WALLETS = [20, 40]

MESSAGE = f"I want to claim my KING tokens on {CHOICE.title()}"


with open("keys.txt") as file:
    keys = [row.strip() for row in file]

if SHUFFLE_KEYS:
    random.shuffle(keys)

with open("proxies.txt") as file:
    proxies = [f"http://{row.strip()}" for row in file]


def sleep(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    desc = datetime.now().strftime("%H:%M:%S")

    for _ in tqdm(range(x), desc=desc, bar_format="{desc} | Sleeping {n_fmt}/{total_fmt}"):
        time.sleep(1)
    print()


def main():
    if not USE_PROXY:
        logger.warning("Not using proxy \n")

    for index, key in enumerate(keys, start=1):
        _id = f"[{index}/{len(keys)}]"
        proxy = proxies[index % len(proxies)] if USE_PROXY else None

        client = Client(_id, key, proxy=proxy)

        if client.get_preference():
            continue

        client.set_preference(message=MESSAGE)

        if index < len(keys):
            sleep(*SLEEP_BETWEEN_WALLETS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Cancelled by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
