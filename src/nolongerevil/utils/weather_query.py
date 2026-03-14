from multidict import MultiDictProxy

from nolongerevil.lib.logger import get_logger
from nolongerevil.lib.types import WeatherQuery

logger = get_logger(__name__)


def parse_query(query: str | MultiDictProxy) -> WeatherQuery | None:
    """
    Parses a raw query string or a multidict proxy into a WeatherQuery object.

    Args:
        query (str | MultiDictProxy): The raw input to parse. This can be a
            formatted string (e.g., "10001,US") or a mapping object typical
            of web framework request parameters (e.g., from aiohttp or multidict).

    Returns:
        WeatherQuery | None: A populated WeatherQuery instance if parsing is
            successful; None if the input is malformed or empty.
    """
    q = None

    if isinstance(query, MultiDictProxy) and "query" in query:
        q = query.get("query")
    elif isinstance(query, str):
        q = query
    if q:
        if "ipv4" in q or "ipv6" in q:
            result = WeatherQuery(postal_code=None, country=None, query_is_ip=True)
            logger.info(f"parsed weather query: '{result}'")
            return result

        parts = q.split(sep=",")
        if parts and len(parts) == 2:
            result = WeatherQuery(postal_code=parts[0], country=parts[1], query_is_ip=False)
            logger.info(f"parsed weather query: '{result}'")
            return result
    return None
