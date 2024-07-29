import os
import requests
import json
from pathlib import Path
from tqdm import tqdm
import internetarchive as ia
from time import sleep

# url = "https://archive.org/download/roosterteeth-api/api/v1/watch.json"
# response = requests.get(url)
# data = response.json()

# url = "https://archive.org/download/roosterteeth-api/api/v1/episodes.json"
# response = requests.get(url)
# data['data'].extend(response.json()['data'])

# url = "https://archive.org/download/roosterteeth-api/api/v1/shows.json"
# response = requests.get(url)
# data['data'].extend(response.json()['data'])

# url = "https://archive.org/download/roosterteeth-api/api/v1/channels.json"
# response = requests.get(url)
# data['data'].extend(response.json()['data'])

# Merge all API endpoints together
with open("api/v1/watch.json", "r") as fp:
    data = json.load(fp)
with open("api/v1/episodes.json", "r") as fp:
    data['data'].extend(json.load(fp)['data'])
with open("api/v1/shows.json", "r") as fp:
    data['data'].extend(json.load(fp)['data'])
with open("api/v1/channels.json", "r") as fp:
    data['data'].extend(json.load(fp)['data'])

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
          verify=True, checksum=True, queue_derive=False, retries=10)

# # Get current list of files on Internet Archive
# already_uploaded = set(x.name for x in ia.get_files("roosterteeth-api-images"))
# print(f"{len(already_uploaded):,} files already uploaded to Internet Archive")

# # Iterate over all files and upload to Internet Archive
# file_count = sum(len(files) for _, _, files in os.walk("image/"))
# with tqdm(total=file_count) as pbar:
#     for root, _, files in os.walk("image/"):
#         for file in files:
#             pbar.update(1)

#             if file == '.DS_Store':
#                 continue

#             filename = os.path.join(root, file)
#             if filename not in already_uploaded:
#                 ia.upload(
#                     identifier="roosterteeth-api-images",
#                     files={filename: filename},
#                     verbose=False,
#                     verify=True,
#                     checksum=True,
#                     queue_derive=False,
#                     retries=10,
#                 )

# # Get current list of files on Internet Archive
# item = ia.get_item("roosterteeth-api-images")
# already_uploaded = set(x.name for x in item.get_files())
# print(f"{len(already_uploaded):,} files already uploaded to Internet Archive")

# # Iterate over all files and upload to Internet Archive
# file_count = sum(len(files) for _, _, files in os.walk("image/"))
# with tqdm(total=file_count) as pbar:
#     for root, _, files in os.walk("image/"):
#         for file in files:
#             pbar.update(1)

#             if file == '.DS_Store':
#                 continue

#             filename = os.path.join(root, file)
#             if filename not in already_uploaded:
#                 item.upload(
#                     files={filename: filename},
#                     verbose=False,
#                     verify=True,
#                     checksum=True,
#                     queue_derive=False,
#                     retries=10,
#                 )

# # Get current list of files on Internet Archive
# item = ia.get_item("roosterteeth-api-images")
# already_uploaded = set(x.name for x in item.get_files())
# print(f"{len(already_uploaded):,} files already uploaded to Internet Archive")

# # Move all uploaded files into separate folder
# count = 0
# for item in already_uploaded:
#     path = Path(item)
#     if path.exists():
#         new_path = item.replace("image/", "image_uploaded/")
#         Path(new_path).parent.mkdir(parents=True, exist_ok=True)
#         path.rename(new_path)
#         count += 1
# print(f"Moved {count:,} files")

# # Iterate over all files and upload to Internet Archive
# # Move uploaded files into separate folder
# item = ia.get_item("roosterteeth-api-images")
# file_count = sum(len(files) for _, _, files in os.walk("image/"))
# print(f"Found {file_count:,} remaining images to upload")
# with tqdm(total=file_count) as pbar:
#     for root, _, files in os.walk("image/"):
#         for file in files:
#             pbar.update(1)

#             if file == '.DS_Store':
#                 continue

#             success = False
#             exception_sleep_time = 60  # seconds
#             while not success:
#                 filename = os.path.join(root, file)
#                 try:
#                     item.upload(
#                         files={filename: filename},
#                         verbose=False,
#                         verify=True,
#                         checksum=True,
#                         queue_derive=True,
#                     )
#                     success = True
#                 except:
#                     print(f"Exception during upload. Sleeping for {exception_sleep_time} seconds")
#                     sleep(exception_sleep_time)
#                     exception_sleep_time *= 2  # Double sleep on each exception

#             new_path = filename.replace("image/", "image_uploaded/")
#             Path(new_path).parent.mkdir(parents=True, exist_ok=True)
#             Path(filename).rename(new_path)

#             sleep(15)
