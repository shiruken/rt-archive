import requests
from urllib.parse import urlencode
from datetime import datetime
import json
import csv
import re
from pathlib import Path


def update_watch():
    """Mirror the Rooster Teeth API /watch endpoint
    - Generates listings for:
      - Internet Archive URL <-> Rooster Teeth URL Mapping (`data/urls.csv`)
        - Rooster Teeth URLs only (`data/rt_urls.txt`)
        - Internet Archive URLs only (`data/archive_urls.txt`)
      - Show Title <-> Show Slug mapping (`data/shows.csv`)
    - Writes intermediary file for RT Archival Checklist (`data/.temp.csv`)
    """
    url = "https://svod-be.roosterteeth.com/api/v1/watch"
    items = get_endpoint(url)
    write_to_json(items, "api/v1/watch.json")

    # Generate derivative listings
    url_map = {}    # IA Item URL -> RT Video URL
    shows = {}      # Show Title -> Show Slug
    checklist = []  # Intermediary data for RT Archival Checklist

    for item in items:
        if item['type'] == "bonus_feature":
            identifier = f"roosterteeth-{item['id']}-bonus"
            show = item['attributes']['parent_content_title'].strip()
            show_slug = item['attributes']['parent_content_slug'].strip()
        else:
            identifier = f"roosterteeth-{item['id']}"
            show = item['attributes']['show_title'].strip()
            show_slug = item['attributes']['show_slug']

        # Manual show name override
        if show == "Grotethe":
            show = "Tales From the Stinky Dragon"

        archive_url = f"https://archive.org/details/{identifier}"
        rt_url = f"https://roosterteeth.com{item['canonical_links']['self']}"
        url_map[archive_url] = rt_url

        if show not in shows:
            shows[show] = show_slug

        date = datetime.fromisoformat(item['attributes']['original_air_date'])
        checklist.append([
            item['attributes']['title'].strip(),
            identifier.replace("roosterteeth-", ""),
            rt_url,
            show,
            date.strftime("%Y-%m-%d"),
            item['attributes']['is_sponsors_only'],
        ])

    with open("data/urls.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(['archive_url', 'rt_url'])
        writer.writerows(url_map.items())

    with open("data/rt_urls.txt", "w") as fp:
        print(*url_map.values(), sep="\n", file=fp)

    with open("data/archive_urls.txt", "w") as fp:
        print(*url_map.keys(), sep="\n", file=fp)

    with open("data/shows.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(['title', 'slug'])
        writer.writerows(sorted(shows.items()))

    with open("data/.temp.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(['title', 'rt_id', 'rt_url', 'show', 'date', 'is_first'])
        writer.writerows(checklist)

    # Update README metrics
    with open("README.md", "r") as fp:
        readme = fp.read()
    readme = re.sub(r"(?<=\* Rooster Teeth Videos: )([\d,]+)", f"{len(url_map):,}", readme)
    with open("README.md", "w") as f:
        f.write(readme)


def update_episodes():
    """Mirror the Rooster Teeth API /episodes endpoint"""
    url = "https://svod-be.roosterteeth.com/api/v1/episodes"
    items = get_endpoint(url)
    write_to_json(items, "api/v1/episodes.json")


def update_shows():
    """Mirror the Rooster Teeth API /shows endpoint"""
    url = "https://svod-be.roosterteeth.com/api/v1/shows"
    items = get_endpoint(url, sort_by_attribute="published_at")
    write_to_json(items, "api/v1/shows.json")


def update_channels():
    """Mirror the Rooster Teeth API /channels endpoint"""
    url = "https://svod-be.roosterteeth.com/api/v1/channels"
    items = get_endpoint(url, sort_by_attribute=None)
    write_to_json(items, "api/v1/channels.json")


def get_endpoint(url, sort_by_attribute='original_air_date'):
    """Returns all values from an endpoint"""
    print(f"Get: {url}")

    items = []
    items_added = set()  # To efficiently avoid duplicates

    page = 1
    while True:
        print(f"Loading Page {page:,}")
        query = {
            'per_page': 1000,
            'page': page
        }
        response = requests.get(f"{url}?{urlencode(query)}")
        json_object = response.json()

        if len(json_object['data']) == 0:
            break

        for item in json_object['data']:
            if item['uuid'] not in items_added:
                items_added.add(item['uuid'])
                items.append(item)

        page += 1

    # Sort by specified attribute + ID to guarantee consistent order.
    # API results are sorted by recency, which causes items with
    # identical timestamps to shuffle around.
    if sort_by_attribute is not None:
        items.sort(key=lambda x: (x['attributes'][sort_by_attribute], x['id']), reverse=True)

    print(f"Loaded {len(items):,} items across {page:,} requests\n")
    return items


def write_to_json(items, filename):
    """Write endpoint data to JSON file"""
    output = {
        "count": len(items),
        "data": items
    }
    with open(filename, "w") as fp:
        json.dump(output, fp)


if __name__ == "__main__":
    Path("api/v1/").mkdir(parents=True, exist_ok=True)
    update_watch()
    update_episodes()
    update_shows()
    update_channels()
