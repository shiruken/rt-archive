import requests
from urllib.parse import urlencode
from internetarchive import get_item
import re
import csv
import pandas as pd
import json
from pathlib import Path
from string import Template


def process():
    """Identify missing, incomplete, and dark Rooster Teeth videos from the Internet Archive
    - Missing RT video URLs: `data/missing.txt`
    - Incomplete Upload URLs: `data/incomplete.csv`
    - Dark (Removed) Upload URLs: `data/dark.csv`
    """
    url = "https://archive.org/services/search/v1/scrape"
    query = {
        'q': 'scanner:"Roosterteeth Website Mirror"',
        'fields': 'identifier,addeddate,item_size,format,incomplete',
        'count': 10000
    }

    archive_items = set()
    incomplete = set()
    total_size = 0

    count = 1
    while True:
        response = requests.get(f"{url}?{urlencode(query)}")
        json = response.json()

        for item in json['items']:
            if (
                "roosterteeth-" in item["identifier"] and
                "roosterteeth-test" not in item["identifier"] and
                "-bonus-bonus" not in item["identifier"] and
                "roosterteeth-52750" not in item['identifier']  # Bad upload
            ):
                archive_items.add(item["identifier"])

                if not (
                    item['item_size'] > 1e6 and
                    "MPEG4" in item['format'] and
                    "JSON" in item['format'] and  # .info.json file
                    "Unknown" in item['format'] and  # .description file
                    (
                        "JPEG" in item['format'] or
                        "PNG" in item['format'] or
                        "Animated GIF" in item['format'] or
                        "JPEG 2000" in item['format'] or
                        "Motion JPEG" in item['format']  # ???
                    ) or item['identifier'] in [  # Items with manually-added WEBP thumbnails
                        "roosterteeth-4277", "roosterteeth-4411", "roosterteeth-4412",
                        "roosterteeth-4433", "roosterteeth-4444",
                    ]
                ) or (
                    'incomplete' in item and item['incomplete'] == "True"
                ):
                    incomplete.add(item['identifier'])

            total_size += item['item_size']

        if 'cursor' in json:
            query['cursor'] = json['cursor']
        else:
            break

        count += 1

    print(f"Identified {len(archive_items):,} items from the Internet Archive Scrape API across {count:,} requests")
    print(f"Total Size: {total_size} bytes")

    urls = {}
    with open("data/urls.csv", "r") as fp:
        reader = csv.reader(fp)
        next(reader)  # Skip header
        for row in reader:
            urls[row[0].replace("https://archive.org/details/", "")] = row[1]

    # Identify items missing from Internet Archive
    missing = [x for x in urls.keys() if x not in archive_items]
    print(f"Found {len(missing):,} items missing from Internet Archive")
    with open("data/missing.txt", "w") as fp:
        for item in missing:
            fp.write(f"{urls[item]}\n")

    # Check whether missing items were removed from Internet Archive
    # Removed = Made 'dark'
    dark = []
    for identifier in missing:
        item = get_item(identifier)
        if item.exists:
            if item.is_dark:
                dark.append(identifier)

    print(f"Found {len(dark):,} dark uploads on Internet Archive")
    with open("data/dark.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(['archive_url', 'rt_url'])
        for item in dark:
            writer.writerow([
                f"https://archive.org/details/{item}",
                f"{urls[item]}"
            ])

    # Mark manually-identified uploads with partial videos as incomplete
    # Listing sourced from RT Archival Checklist project
    with open("data/partial_videos.txt", "r") as fp:
        for line in fp.readlines():
            incomplete.add(line.rstrip())

    print(f"Found {len(incomplete):,} incomplete items on Internet Archive")
    with open("data/incomplete.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(['archive_url', 'rt_url'])
        for item in sorted(incomplete):
            writer.writerow([
                f"https://archive.org/details/{item}",
                f"{urls[item]}"
            ])

    # Update README metrics
    with open("README.md", "r") as fp:
        readme = fp.read()
    readme = re.sub(r"(?<=\* Items Uploaded to Internet Archive: )([\d, \(.\%\)]+)", f"{len(archive_items) + len(dark):,} ({(len(archive_items) + len(dark)) / len(urls):.3%})", readme)
    readme = re.sub(r"(?<=\* Items Missing from Internet Archive: )([\d, \(.\%\)]+)", f"{len(missing) - len(dark):,} ({(len(missing) - len(dark)) / len(urls):.3%})", readme)
    readme = re.sub(r"(?<=\* Incomplete Items on Internet Archive: )([\d, \(.\%\)]+)", f"{len(incomplete):,} ({len(incomplete) / len(urls):.3%})", readme)
    readme = re.sub(r"(?<=\* Items Removed from Internet Archive: )([\d, \(.\%\)]+)", f"{len(dark):,} ({len(dark) / len(urls):.3%})", readme)
    readme = re.sub(r"(?<=\* Overall Archive Availability: )([\d.\%]+)", f"{(1 - (len(missing) + len(incomplete)) / len(urls)):.3%}", readme)
    with open("README.md", "w") as f:
        f.write(readme)

    # Generate CSV file for RT Archival Checklist
    # - Requires intermediary file (`data/.temp.csv`) generated by `update_rt.py`
    # - Writes output to `data/checklist.csv`
    # Columns: title, rt_id, rt_url, show, date, is_first, is_uploaded, is_complete_upload, is_removed
    with open("data/.temp.csv", "r") as input, open("data/checklist.csv", "w") as output:
        reader = csv.reader(input)
        writer = csv.writer(output)

        checklist = []
        header = next(reader)
        header.extend(['is_uploaded', 'is_complete_upload', 'is_removed'])
        checklist.append(header)

        for row in reader:
            identifier = f"roosterteeth-{row[1]}"
            is_uploaded = identifier not in missing
            is_complete_upload = is_uploaded and identifier not in incomplete
            is_removed = identifier in dark
            row.extend([is_uploaded, is_complete_upload, is_removed])
            checklist.append(row)

        writer.writerows(checklist)


def generate_website():
    """Generates Archive Progress website"""

    df = pd.read_csv("data/checklist.csv")
    df_show_slugs = pd.read_csv("data/shows.csv", index_col="title")

    with open("docs/_template.html", "r") as fp:
        html = fp.read()
    html_template = MyTemplate(html)

    def process_shows(df):
        slug = df_show_slugs.loc[df.name].values[0]
        summary = generate_summary(df)
        show = pd.concat([pd.Series(slug, index=["slug"]), summary])
        process_episodes(df, slug)
        return show

    def process_episodes(df, show_slug):
        summary = generate_summary(df)
        df['rt_url'] = df['rt_url'].str.replace(r'https://roosterteeth.com/watch/', "")
        df.rename(columns={'rt_id': 'id', 'rt_url': 'slug'}, inplace=True)

        output = {
            "show": df.name,
            "slug": show_slug,
            "summary": summary.to_dict(),
            "data": df.to_dict(orient="records"),
        }
        Path(f"docs/{show_slug}/").mkdir(parents=True, exist_ok=True)
        with open(f"docs/{show_slug}/data.json", "w") as fp:
            json.dump(output, fp, indent=4)

        search_show_title = df.name
        if search_show_title == "Tales from the Stinky Dragon":
            search_show_title = "Grotethe"
        query = {
            'query': f'scanner:"Roosterteeth Website Mirror" AND show_title:"{search_show_title}"',
            'sort': '-date'
        }
        show_search_url = f"https://archive.org/search?{urlencode(query)}"
        html_new = html_template.substitute({
            "show": df.name,
            "show_slug": show_slug,
            "show_search_url": show_search_url,
        })
        with open(f"docs/{show_slug}/index.html", "w") as fp:
            fp.write(html_new)

    def generate_summary(df):
        output = {}
        output['count'] = df['rt_id'].count()
        output['uploaded'] = df['is_uploaded'].sum() + df['is_removed'].sum()
        output['missing'] = output['count'] - output['uploaded']
        output['incomplete'] = output['uploaded'] - df['is_complete_upload'].sum() - df['is_removed'].sum()
        output['removed'] = df['is_removed'].sum()
        return pd.Series(output)

    df_shows = df.groupby("show").apply(process_shows, include_groups=False)
    df_shows.sort_index(key=lambda x: x.str.lower(), inplace=True)
    summary = generate_summary(df)

    output = {
        "summary": summary.to_dict(),
        "data": df_shows.reset_index().to_dict(orient="records"),
    }
    with open("docs/data.json", "w") as fp:
        json.dump(output, fp, indent=4)

    # Generate data for missing page
    df_missing = df[~df['is_uploaded'] & ~df['is_removed']].copy()
    df_missing['rt_url'].to_csv("docs/missing/missing.csv", index=False)
    df_missing['rt_url'] = df_missing['rt_url'].str.replace(r'https://roosterteeth.com/watch/', "")
    df_missing = df_missing.merge(df_show_slugs, left_on="show", right_index=True)
    df_missing.rename(columns={'rt_id': 'id', 'rt_url': 'slug', 'slug': 'show_slug'}, inplace=True)
    df_missing = df_missing[['title', 'slug', 'date', 'is_first', 'show', 'show_slug']]
    output = {
        "count": df_missing.shape[0],
        "data": df_missing.to_dict(orient="records"),
    }
    with open("docs/missing/data.json", "w") as fp:
        json.dump(output, fp, indent=4)

    # Generate data for incomplete page
    df_incomplete = df[~df['is_complete_upload'] & df['is_uploaded']& ~df['is_removed']].copy()
    df_incomplete['rt_url'] = df_incomplete['rt_url'].str.replace(r'https://roosterteeth.com/watch/', "")
    df_incomplete = df_incomplete.merge(df_show_slugs, left_on="show", right_index=True)
    df_incomplete.rename(columns={'rt_id': 'id', 'rt_url': 'slug', 'slug': 'show_slug'}, inplace=True)
    df_incomplete = df_incomplete[['id', 'title', 'slug', 'date', 'is_first', 'show', 'show_slug']]
    output = {
        "count": df_incomplete.shape[0],
        "data": df_incomplete.to_dict(orient="records"),
    }
    with open("docs/incomplete/data.json", "w") as fp:
        json.dump(output, fp, indent=4)
    df_archive_links = "https://archive.org/details/roosterteeth-" + df_incomplete['id']
    df_rt_links = "https://roosterteeth.com/watch/" + df_incomplete['slug']
    df_links = pd.concat([df_archive_links, df_rt_links], axis=1, keys=['archive_url', 'rt_url'])
    df_links.to_csv("docs/incomplete/incomplete.csv", index=False)

    # Generate data for removed page
    df_removed = df[df['is_removed']].copy()
    df_removed['rt_url'] = df_removed['rt_url'].str.replace(r'https://roosterteeth.com/watch/', "")
    df_removed = df_removed.merge(df_show_slugs, left_on="show", right_index=True)
    df_removed.rename(columns={'rt_id': 'id', 'rt_url': 'slug', 'slug': 'show_slug'}, inplace=True)
    df_removed = df_removed[['id', 'title', 'slug', 'date', 'is_first', 'show', 'show_slug']]
    output = {
        "count": df_removed.shape[0],
        "data": df_removed.to_dict(orient="records"),
    }
    with open("docs/removed/data.json", "w") as fp:
        json.dump(output, fp, indent=4)
    df_archive_links = "https://archive.org/details/roosterteeth-" + df_removed['id']
    df_rt_links = "https://roosterteeth.com/watch/" + df_removed['slug']
    df_links = pd.concat([df_archive_links, df_rt_links], axis=1, keys=['archive_url', 'rt_url'])
    df_links.to_csv("docs/removed/removed.csv", index=False)


class MyTemplate(Template):
    delimiter = '$$'


if __name__ == "__main__":
    process()
    generate_website()
