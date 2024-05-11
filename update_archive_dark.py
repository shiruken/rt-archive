from internetarchive import get_item
import re
import csv


def identify_dark():
    """Identify 'dark' uploads that have been removed by Internet Archive

    Writes dark URLs to `data/dark.csv`
    """
    with open("data/missing.txt", "r") as fp:
        missing = [line.rstrip() for line in fp]

    urls = {}
    with open("data/urls.csv", "r") as fp:
        reader = csv.reader(fp)
        next(reader)  # Skip header
        for row in reader:
            urls[row[1]] = row[0].replace("https://archive.org/details/", "")

    dark = []
    for rt_url in missing:
        identifier = urls[rt_url]
        item = get_item(identifier)
        if item.exists:
            if item.is_dark:
                archive_url = f"https://archive.org/details/{identifier}"
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
