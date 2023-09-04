import requests
from dateutil import parser
import datetime
URL = "https://az.wikipedia.org/w/api.php"

def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microsecond)

def get_data_from_api(params):
    try:
        response = requests.get(url=URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def is_template_outdated(page):
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": page['title'],
        "rvslots": "main",
        "formatversion": "2",
        "format": "json"
    }
    data = get_data_from_api(params)

    if not data:
        return False

    pages = data.get("query", {}).get("pages", [])
    if pages:
        revision = pages[0].get("revisions", [])[0]
        if revision:
            insertion_date = parser.parse(revision.get("timestamp", ""))
            right_now_7_days_ago = datetime.datetime.today() - datetime.timedelta(days=7)

            if insertion_date.replace(tzinfo=None) < chop_microseconds(right_now_7_days_ago):
                return True

    return False

def main():
    params = {
        "action": "query",
        "cmtitle": "Kateqoriya:İş_davam_edən_səhifələr",
        "cmlimit": "200",
        "list": "categorymembers",
        "format": "json"
    }
    data = get_data_from_api(params)

    if not data:
        return

    pages = data.get("query", {}).get("categorymembers", [])
    for page in pages:
        if is_template_outdated(page):
            print(u'\u2713', page['title'], "şablon silinməlidir")
        else:
            print(u'\u2717', page['title'], "şablon silinməməlidir")

if __name__ == "__main__":
    main()