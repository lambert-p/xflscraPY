from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import json

def calculate_num_games():
    """
    TODO Actually make this robust. Just worried about getting the
    data processing working for now.
    """
    return 8

def fetch_pbp(url):
    """
    Attempts to get the content at `url' by making an HTTP GET request.
    If the content-type of response is HTML/XML return content; otherwise
    return None.
    """

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                resp = resp.text
                start = resp.find('playList = ') + len('playList = ')
                end = resp.find('</script>', start)
                live_stats = resp[start:end]
                return live_stats
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
        data = fetch_pbp(url)
        print(data)

if __name__ == '__main__':
    main()
    
