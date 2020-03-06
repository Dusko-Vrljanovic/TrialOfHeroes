import os
import argparse
import sys
from multiprocessing import Pool

from download import filter_albums, get_request_json, download_photo

URL = "https://jsonplaceholder.typicode.com/"
ALBUMS_ENDPOINT = "albums"
PHOTOS_ENDPOINT = "photos"
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Console app that filters albums \
        by “title” field, specified from the command line. Downloads all the photos \
        in the matched albums. Separates images by folder, where folder name is generated \
        by the pattern specified from the command line (default “album-{albumId}”. \
        Folders are created in the root directory of the script location."
    )
    
    parser.add_argument("--filter", required=True, help="<regex_str> Regex to filter albums")
    parser.add_argument("--dest-dir-pattern", 
                        help="<str> Folder name suffix (default: resolves ‘album-{albumId}’)"
                        )

    args = parser.parse_args()
    

    regex_str = args.filter
    default_album_name = True if args.dest_dir_pattern is None else False

    album_name = None
    if default_album_name is False:
        album_name = "album-{}".format(args.dest_dir_pattern)

    filtered_albums = filter_albums(URL, ALBUMS_ENDPOINT, regex_str, default_album_name, BASE_DIR)
    if filtered_albums is not None:
        photos_for_download = []
        photos = get_request_json(URL, PHOTOS_ENDPOINT)
        if photos is not None:
            for photo in photos:
                if photo["albumId"] in filtered_albums:
                    if default_album_name is True:
                        album_name = "album-{}".format(photo["albumId"])
                    photo["destination"] = os.path.join(BASE_DIR, album_name)

                    photos_for_download.append(photo)

        if default_album_name is False:    
            if not os.path.isdir(os.path.join(BASE_DIR, album_name)):
                os.makedirs(os.path.join(BASE_DIR, album_name))
        
        # for photo in photos_for_download:
        #     download_photo(photo)

        with Pool() as pool:
            pool.map(download_photo, photos_for_download)

