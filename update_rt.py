import requests
from urllib.parse import urlencode
import json


def update_watch():
    """Mirror the Rooster Teeth API /watch endpoint.

    Writes all results to `data/watch.json`

    Also generates listings for:
      - Every Rooster Teeth website video URL (`data/rt_urls.txt`)
      - Every Internet Archive item URL (`data/archive_urls.txt`)
    """
    url = "https://svod-be.roosterteeth.com/api/v1/watch"
    page = 1

    # results = []   # Complete API listing
    archive_map = {}  # IA Item URL -> RT Video URL

    while True:
        query = {
            'per_page': 1000,
            'page': page
        }
        response = requests.get(f"{url}?{urlencode(query)}")
        json_object = response.json()

        if len(json_object['data']) == 0:
            break

        for item in json_object['data']:

            identifier = f"https://archive.org/details/roosterteeth-{item['id']}"
            if item['type'] == "bonus_feature":
                identifier += "-bonus"

            if identifier not in archive_map:
                # results.append(item)
                archive_map[identifier] = f"https://roosterteeth.com/watch/{item['attributes']['slug']}"

        page += 1

    print(f"Identified {len(archive_map):,} unique items from the Rooster Teeth API across {page:,} requests")

    # output = {
    #     "count": len(results),
    #     "data": results
    # }
    # with open("data/watch.json", "w") as fp:
    #     json.dump(output, fp)

    with open("data/rt_urls.txt", "w") as fp:
        print(*archive_map.values(), sep="\n", file=fp)

    with open("data/archive_urls.txt", "w") as fp:
        print(*archive_map.keys(), sep="\n", file=fp)


if __name__ == "__main__":
    update_watch()
