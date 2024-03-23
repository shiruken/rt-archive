import requests
import json

api_url = "https://svod-be.roosterteeth.com/api/v1/watch"
per_page = 1000
page = 1

watch_items = []
rt_urls = []
archive_ids = []

while True:
    response = requests.get(f"{api_url}?per_page={per_page}&page={page}")
    json_object = response.json()

    if len(json_object['data']) == 0:
        break

    for item in json_object['data']:

        identifier = f"roosterteeth-{item['id']}"
        if item['type'] == "bonus_feature":
            identifier += "-bonus"

        if identifier not in archive_ids:
            watch_items.append(item)
            rt_urls.append(f"https://roosterteeth.com/watch/{item['attributes']['slug']}")
            archive_ids.append(identifier)

    page += 1

print(f"Identified {len(archive_ids):,} unique items from {page:,} requests")

watch = {
    "count": len(watch_items),
    "data": watch_items
}
with open("watch.json", "w") as fp:
    json.dump(watch, fp)

with open("rt_urls.txt", "w") as fp:
    print(*rt_urls, sep="\n", file=fp)

with open("archive_ids.txt", "w") as fp:
    print(*archive_ids, sep="\n", file=fp)
