import requests
from urllib.parse import urlencode
import re


def identify_missing_incomplete():
    """Identify missing and incomplete Rooster Teeth videos from the Internet Archive

    Writes missing video URLs to `data/missing.txt`

    Writes incomplete upload URLs to `data/incomplete_rt.txt` and `data/incomplete_archive.txt`
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
        json = response.json()

        for item in json['items']:
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
                        "Animated GIF" in item['format'] or
                        "JPEG 2000" in item['format']
                    )
                ):
                    incomplete.append(item['identifier'])

        if 'cursor' in json:
            query['cursor'] = json['cursor']
        else:
            break

        count += 1

    print(f"Identified {len(archive_items):,} items from the Internet Archive Scrape API across {count:,} requests")

    with open("data/archive_urls.txt", "r") as fp:
        archive_ids = [line.rstrip().replace("https://archive.org/details/", "") for line in fp]

    with open("data/rt_urls.txt", "r") as fp:
        rt_urls = [line.rstrip() for line in fp]

    archive_items = set(archive_items)
    missing = [x for x in archive_ids if x not in archive_items]
    print(f"Found {len(missing):,} items missing from Internet Archive")
    with open("data/missing.txt", "w") as fp:
        for item in missing:
            fp.write(f"{rt_urls[archive_ids.index(item)]}\n")

    print(f"Found {len(incomplete):,} incomplete items on Internet Archive")
    with open("data/incomplete_rt_urls.txt", "w") as fp:
        for item in incomplete:
            fp.write(f"{rt_urls[archive_ids.index(item)]}\n")
    with open("data/incomplete_archive_urls.txt", "w") as fp:
        for item in incomplete:
            fp.write(f"https://archive.org/details/{item}\n")

    with open("README.md", "r") as fp:
        readme = fp.read()
    readme = re.sub(r"(?<=\* Items on Internet Archive: )([\d,]+)", f"{len(archive_items):,}", readme)
    readme = re.sub(r"(?<=\* Items Missing from Internet Archive: )([\d,]+)", f"{len(missing):,}", readme)
    readme = re.sub(r"(?<=\* Incomplete Items on Internet Archive: )([\d,]+)", f"{len(incomplete):,}", readme)
    with open("README.md", "w") as f:
        f.write(readme)


if __name__ == "__main__":
    identify_missing_incomplete()
