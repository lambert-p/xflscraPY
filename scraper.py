from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def calculate_num_games():
    """
    TODO Actually make this robust. Just worried about getting the
    data processing working for now.
    """
    return 8

def simple_get(url):
    """
    Attempts to get the content at `url' by making an HTTP GET request.
    If the content-type of response is HTML/XML return content; otherwise
    return None.
    """

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1} ' . format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)
    

def main():
    num_games = calculate_num_games()
    for match in range(1, num_games+1):
        print("We're getting the data for Match %d" % (match))
        url = "https://stats.xfl.com/" + str(match)
        data = simple_get(url)
        print(data)

if __name__ == '__main__':
    main()
    
