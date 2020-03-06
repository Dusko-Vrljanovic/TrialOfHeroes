import requests
import re
import os
import random

def get_request_json(url, endpoint):
    json = None
    try:
        response = requests.get(url + endpoint)
        response.raise_for_status()
        if response.status_code == 200:
            json = response.json()
            
    except requests.exceptions.HTTPError as http_error:
        print("HTTP Error: ", http_error)
    except requests.exceptions.ConnectionError as connection_error: 
        print ("Error Connecting: ", connection_error) 
    except requests.exceptions.Timeout as timeout_error: 
        print ("Timeout Error:", timeout_error) 
    except requests.exceptions.RequestException as request_exception: 
        print ("Something Else:", request_exception)

    return json

def get_request_content(url):
    content = None
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            content = response.content
            
    except requests.exceptions.HTTPError as http_error:
        print("HTTP Error: ", http_error)
    except requests.exceptions.ConnectionError as connection_error: 
        print ("Error Connecting: ", connection_error) 
    except requests.exceptions.Timeout as timeout_error: 
        print ("Timeout Error:", timeout_error) 
    except requests.exceptions.RequestException as request_exception: 
        print ("Something Else:", request_exception)

    return content

def filter_albums(url, endpoint, regex_str, default_album_name=True, base_dir=""):
    albums = get_request_json(url, endpoint)
    
    if albums is not None:
        filtered_albums = []
        
        for album in albums:
            if re.search(regex_str, album["title"]) is not None:      
                filtered_albums.append(album["id"])
                
                if default_album_name is True:
                    temp_album_name = "album-{}".format(album["id"])
                    if not os.path.isdir(os.path.join(base_dir, temp_album_name)):
                        os.makedirs(os.path.join(base_dir, temp_album_name))

        return filtered_albums
    else:
        return albums

def download_photo(photo):
    destination = photo["destination"]
    url = photo["url"]

    photo_name = url.split("/")[-1]
    photo_path = os.path.join(destination, photo_name + ".jpg")
    while os.path.isfile(photo_path):
        new_name = photo_name + str(random.randint(0, 1000))
        photo_path = os.path.join(destination, new_name + ".jpg")

    print("{} download started ...".format(photo_name))
    photo = get_request_content(url)
    if photo is not None:
        with open(photo_path, "wb") as photo_file:
            photo_file.write(photo)
        print("{} download ended.".format(photo_name))
    else:
        print("{} download failed.".format(photo_name))
    