from internetarchive import get_item
import re
import csv


def identify_dark():
    """Identify 'dark' uploads that have been removed by Internet Archive

    Writes dark URLs to `data/dark.csv`
    """
    with open("data/missing.txt", "r") as fp:
        missing = [line.rstrip() for line in fp]

    with open("data/archive_urls.txt", "r") as fp:
        archive_urls = [line.rstrip() for line in fp]

    with open("data/rt_urls.txt", "r") as fp:
        rt_urls = [line.rstrip() for line in fp]

    dark = []
    for rt_url in missing:
        index = rt_urls.index(rt_url)
        archive_url = archive_urls[index]
        identifier = archive_url.replace("https://archive.org/details/", "")
        item = get_item(identifier)
        if item.exists:
            if item.is_dark:
                print(f"{archive_url} is dark ({rt_url})")
                dark.append([archive_url, rt_url])

    print(f"Found {len(dark):,} dark uploads on Internet Archive")

    with open("data/dark.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(['archive_url', 'rt_url'])
        writer.writerows(dark)

    # Update README metrics
    with open("README.md", "r") as fp:
        readme = fp.read()
    readme = re.sub(r"(?<=\* Items Removed from Internet Archive: )([\d,]+)", f"{len(dark):,}", readme)
    with open("README.md", "w") as f:
        f.write(readme)


if __name__ == "__main__":
    identify_dark()
