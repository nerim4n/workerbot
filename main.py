import requests
from dateutil import parser
from datetime import datetime, timedelta

URL = "https://az.wikipedia.org/w/api.php"

def get_data_from_api(params):
    try:
        response = requests.get(url=URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def is_template_outdated(page):
    # Existing code for checking if the template is outdated
    # ...

def remove_specific_text_from_page(page_content):
    # Modify this function to remove specific text from the page content
    # For example, replace "TextToRemove" with an empty string to remove it
    return page_content.replace("TextToRemove", "")

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

            # Fetch the current page content
            content_params = {
                "action": "query",
                "prop": "revisions",
                "titles": page['title'],
                "rvslots": "main",
                "formatversion": "2",
                "format": "json"
            }
            content_data = get_data_from_api(content_params)
            
            if content_data:
                pages = content_data.get("query", {}).get("pages", [])
                if pages:
                    revision = pages[0].get("revisions", [])[0]
                    if revision:
                        page_content = revision.get("slots", {}).get("main", {}).get("content", "")

                        # Remove specific text if condition is true
                        modified_content = remove_specific_text_from_page(page_content)
                        
                        # Update the page content
                        edit_params = {
                            "action": "edit",
                            "title": page['title'],
                            "token": "YOUR_EDIT_TOKEN",  # Obtain the edit token (similar to previous examples)
                            "text": modified_content,
                            "summary": "Edit via API",
                            "format": "json"
                        }
                        edit_response = get_data_from_api(edit_params)
                        
                        if edit_response and edit_response.get("edit", {}).get("result") == "Success":
                            print(f"Removed specific text from '{page['title']}'")
                        else:
                            print(f"Failed to remove specific text from '{page['title']}'")
        else:
            print(u'\u2717', page['title'], "şablon silinməməlidir")

if __name__ == "__main__":
    main()
