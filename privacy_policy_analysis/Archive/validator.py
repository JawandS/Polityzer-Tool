# go through manual downloads and note any empty files or 301 redirects
import os

for office in os.listdir("manual_downloads"):
    # log the number
    print(f"{office}: {len(os.listdir(f'manual_downloads/{office}'))}")
    # go through files
    for candidate in os.listdir(f"manual_downloads/{office}"):
        if os.stat(f"manual_downloads/{office}/{candidate}").st_size == 0:
            print(f"Empty file: {candidate}")
        else:
            with open(f"manual_downloads/{office}/{candidate}", "r") as f:
                try:
                    if "301 Moved Permanently" in f.read():
                        print(f"301 redirect: {candidate}")
                except:
                    print(f"Error: {candidate}")

