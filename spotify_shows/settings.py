import logging
import os

# Log configuration
logger = logging.getLogger("spotify_shows")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

FROM_DOCKER = os.getenv("FROM_DOCKER", False)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.97 Safari/537.36",
}
EXTRA_HTTP_HEADERS = {"Accept-Language": "en-US;q=0.8,en;q=0.7"}

WAIT_COND = ["domcontentloaded", "networkidle0"]

OPENAI_MODEL = "gpt-3.5-turbo"

LOCATION = os.getenv("LOCATION", "California")