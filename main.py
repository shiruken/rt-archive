import requests
from urllib.parse import urlencode
import json


def update_watch() -> dict:
    """Process the Rooster Teeth API /watch endpoint.

    Writes all results to `data/watch.json`

    Also generates listings for:
      - Every website video URL (`data/rt_urls.txt`)
      - Internet Archive identifiers for every video (`data/archive_ids.txt`)
    """
    url = "https://svod-be.roosterteeth.com/api/v1/watch"
    page = 1

    results = []   # Complete API listing
    ia_rt_map = {}  # IA Identifer -> RT Video URL

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

            identifier = f"roosterteeth-{item['id']}"
            if item['type'] == "bonus_feature":
                identifier += "-bonus"

            if identifier not in ia_rt_map:
                results.append(item)
                ia_rt_map[identifier] = f"https://roosterteeth.com/watch/{item['attributes']['slug']}"

        page += 1

    print(f"Identified {len(ia_rt_map):,} unique items from the Rooster Teeth API across {page:,} requests")

    output = {
        "count": len(results),
        "data": results
    }
    with open("data/watch.json", "w") as fp:
        json.dump(output, fp)

    with open("data/rt_urls.txt", "w") as fp:
        print(*ia_rt_map.values(), sep="\n", file=fp)

    with open("data/archive_ids.txt", "w") as fp:
        print(*ia_rt_map.keys(), sep="\n", file=fp)

    return ia_rt_map


def identify_missing_incomplete(ia_rt_map: dict):
    """Identify missing and incomplete Rooster Teeth videos from the Internet Archive

    Writes results to `data/archive_missing.txt` and `data/archive_incomplete.txt`
    """
    url = "https://archive.org/services/search/v1/scrape"
    query = {
        'q': 'scanner:"Roosterteeth Website Mirror"',
        'fields': 'identifier,addeddate,item_size,format',
        'count': 10000
    }

    archive_items = []
    incomplete = []

    count = 1
    while True:
        response = requests.get(f"{url}?{urlencode(query)}")
        json_object = response.json()

        for item in json_object['items']:
            if (
                "roosterteeth-" in item["identifier"] and
                "roosterteeth-test" not in item["identifier"] and
                "-bonus-bonus" not in item["identifier"]
            ):
                archive_items.append(item["identifier"])

                if not (
                    "MPEG4" in item['format'] and
                    "JSON" in item['format'] and # .info.json file
                    "Unknown" in item['format'] and # .description file
                    (
                        "JPEG" in item['format'] or
                        "PNG" in item['format'] or
                        "Animated GIF" in item['format']
                    )
                ):
                    incomplete.append(item['identifier'])

        if 'cursor' in json_object:
            query['cursor'] = json_object['cursor']
        else:
            break

        count += 1

    print(f"Identified {len(archive_items):,} items from the Internet Archive Scrape API across {count:,} requests")

    missing = set(ia_rt_map.keys()) - set(archive_items)
    print(f"Found {len(missing):,} items missing from Internet Archive")
    with open("data/archive_missing.txt", "w") as fp:
        for item in missing:
            fp.write(f"{ia_rt_map[item]}\n")

    print(f"Found {len(incomplete):,} incomplete items on Internet Archive")
    with open("data/archive_incomplete.txt", "w") as fp:
        for item in incomplete:
            fp.write(f"{ia_rt_map[item]}\n")


if __name__ == "__main__":
    ia_rt_map = update_watch()
    identify_missing_incomplete(ia_rt_map)
