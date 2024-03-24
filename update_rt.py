import requests
from urllib.parse import urlencode
from datetime import datetime
import json
import csv
import os
from internetarchive import upload


def update_watch():
    """Mirror the Rooster Teeth API /watch endpoint.

    Writes all results to `api/v1/watch.json`

    Also generates listings for:
      - Every Rooster Teeth website video URL (`data/rt_urls.txt`)
      - Every Internet Archive item URL (`data/archive_urls.txt`)
      - RT Archival Checklist (`data/checklist.csv`)
    """
    url = "https://svod-be.roosterteeth.com/api/v1/watch"
    page = 1

    results = []         # Complete API listing
    archive_map = {}     # IA Item URL -> RT Video URL
    checklist_data = []  # Data for RT Archival Checklist

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
            archive_url = f"https://archive.org/details/{identifier}"

            if archive_url not in archive_map:
                results.append(item)

                rt_url = f"https://roosterteeth.com{item['canonical_links']['self']}"
                archive_map[archive_url] = rt_url

                if item['type'] == "bonus_feature":
                    show = item['attributes']['parent_content_title'].strip()
                else:
                    show = item['attributes']['show_title'].strip()

                date = datetime.strptime(item['attributes']['original_air_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                checklist_data.append([
                    item['attributes']['title'].strip(),
                    identifier.replace("roosterteeth-", ""),
                    rt_url,
                    show,
                    date.strftime("%Y-%m-%d"),
                    item['attributes']['is_sponsors_only']
                ])

        page += 1

    print(f"Identified {len(archive_map):,} unique items from the Rooster Teeth API across {page:,} requests")

    output = {
        "count": len(results),
        "data": results
    }
    with open("api/v1/watch.json", "w") as fp:
        json.dump(output, fp)

    with open("data/rt_urls.txt", "w") as fp:
        print(*archive_map.values(), sep="\n", file=fp)

    with open("data/archive_urls.txt", "w") as fp:
        print(*archive_map.keys(), sep="\n", file=fp)

    with open("data/checklist.csv", "w", newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(checklist_data)


def upload_to_ia():
    """Upload contents of api/ directory to Internet Archive"""
    access_key = os.getenv("IA_ACCESS_KEY")
    secret_key = os.getenv("IA_SECRET_KEY")
    upload(
        identifier="roosterteeth-api",
        files="api",
        access_key=access_key,
        secret_key=secret_key,
        verify=True,
        checksum=True,
        verbose=True,
        retries=9,
    )


if __name__ == "__main__":
    update_watch()
    try:
        upload_to_ia()
    except Exception as e:
        print(f"Error uploading to Internet Archive: {e}")
