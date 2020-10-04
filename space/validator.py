from urllib.parse import urlparse
import re 

def validate_url(url:str)-> str:
    '''
    Returns url if valid or raises ValueError
    params:
        url:str
    returns:
        url:str
    '''
    parsed = urlparse(url)
    regex = re.compile('/threads/[a-z\-]+.[0-9]+/?')
    if parsed.scheme != 'https':
        raise ValueError('Wrong link Type')
    if parsed.netloc != 'forums.spacebattles.com':
        raise ValueError('Wrong link Type')
    if not regex.fullmatch(parsed.path):
        raise ValueError('Wrong link Type')
    if url.endswith('/'):
        url.rstrip('/')
    return url


