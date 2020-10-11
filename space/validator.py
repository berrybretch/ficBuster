from urllib.parse import urlparse
import re


def validate_url(url: str) -> str:
    """
    Returns url if valid or raises ValueError
    params:
        url:str
    returns:
        url:str
    """
    if not url:
        return ValueError("url is empty")
    else:
        parsed = urlparse(url)
        regex = re.compile("/threads/[a-z0-9\-]+.[0-9]+/reader/?")
        if parsed.scheme != "https":
            raise ValueError("Not https")
        if parsed.netloc != "forums.spacebattles.com":
            raise ValueError("Wrong net location")
        if not regex.fullmatch(parsed.path):
            raise ValueError("Need the reader link")
        if url.endswith("/"):
            url = url.rstrip("/")
    return url
