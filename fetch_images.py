import os
import requests
from pathlib import Path
from tqdm import tqdm
import internetarchive as ia

url = "https://archive.org/download/roosterteeth-api/api/v1/watch.json"
response = requests.get(url)
data = response.json()

url = "https://archive.org/download/roosterteeth-api/api/v1/episodes.json"
response = requests.get(url)
data['data'].extend(response.json()['data'])

url = "https://archive.org/download/roosterteeth-api/api/v1/shows.json"
response = requests.get(url)
data['data'].extend(response.json()['data'])

url = "https://archive.org/download/roosterteeth-api/api/v1/channels.json"
response = requests.get(url)
data['data'].extend(response.json()['data'])

print(f"Loaded {len(data['data']):,} API items")

# Download all images, skip existing
count = 0
unique = set()
unique_error = set()
for item in tqdm(data['data']):

    for image in item['included']['images']:
        for size in ['thumb', 'small', 'medium', 'large']:
            image_url = image['attributes'].get(size)

            count += 1
            unique.add(image_url)

            if "s3.amazonaws.com" in image_url:
                path = image_url.replace("https://s3.amazonaws.com/dev.cdn.roosterteeth.com/", "image/")
            else:
                path = image_url.replace("https://cdn.roosterteeth.com/", "")

            file = Path(path)
            if not file.is_file():
                response = requests.get(image_url)
                if response.status_code == 200:
                    file.parent.mkdir(parents=True, exist_ok=True)
                    with open(file, 'wb') as fp:
                        fp.write(response.content)
                else:
                    unique_error.add(image_url)

print(f"Processed {count:,} image urls ({len(unique):,} unique urls)")

# Write broken URLs to file
print(f"Unable to download {len(unique_error):,} files (see fetch_images_broken.txt)")
with open("fetch_images_broken.txt", "w") as fp:
    fp.write("\n".join(unique_error))

# Purge macOS .DS_Store files
count = 0
for root, dirs, files in os.walk("image/"):
    for file in files:
        if file == '.DS_Store':
            os.remove(os.path.join(root, file))
            count += 1

print(f"Purged {count:,} .DS_Store files")

# Upload to Internet Archive
ia.upload(identifier="roosterteeth-api-images", files="image", verbose=True,
          verify=True, checksum=True, queue_derive=True, retries=10)

