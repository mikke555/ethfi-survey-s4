from datetime import datetime
from sys import stderr

from fake_useragent import UserAgent
from loguru import logger

now = datetime.now()

logger.remove()
logger.add(
    stderr,
    format="<white>{time:HH:mm:ss}</white> | <level>{message}</level>",
)
logger.add(
    sink=f"{now:%Y-%m-%d}.log",
    format="<white>{time:HH:mm:ss}</white> | <level>{message}</level>",
)


headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "referer": "https://app.ether.fi/portfolio",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": UserAgent().random,
}
