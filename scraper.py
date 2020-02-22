"""
scraper.py

Script scrapes XFL play-by-play data from their website,
and formats it into an identical form as nflscrapR does for
NFL data. For use by hobbyists wishing to do statistical
analysis on XFL data.

@author Paul Lambert <paul dot lambert at linux dot com>

"""
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
    If the content-type of response is valid, process and return it as JSON; 
    otherwise return None.
    """

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                resp = resp.text

                # our JSON PBP data is stored in a JavaScript var playList
                start = resp.find('playList = ') + len('playList = ')
                end = resp.find('</script>', start)

                # substring and clean the JSON before returning
                pbp = resp[start:end]
                pbp = pbp.strip()
                pbp = pbp[:-1] # remove trailing semicolon from the JS

                return json.loads(pbp)
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

def format_json_for_csv(json_data):
    """
    Attempts to mimic the format used by the very popular package
    for providing NFL CSVs, nflscrapR. 

    Converts the play by play data from scraped JSON into CSV
    
    See https://github.com/maksimhorowitz/nflscrapR for more information
    """
    return json_data

def main():
    num_games = calculate_num_games()

    for match in range(1, num_games+1):
        print("We're getting the data for Match %d" % (match))
        url = "https://stats.xfl.com/" + str(match)
        json_data = fetch_pbp(url)
        print(json_data)
        csv_data = format_json_for_csv(json_data)

if __name__ == '__main__':
    main()
    
