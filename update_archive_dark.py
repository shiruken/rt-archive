from internetarchive import get_item


def identify_dark():
    """Identify 'dark' uploads that have been removed by Internet Archive

    Writes dark upload URLs to `data/dark.txt`
    """
    with open("data/missing.txt", "r") as fp:
        missing = [line.rstrip() for line in fp]

    with open("data/archive_urls.txt", "r") as fp:
        archive_urls = [line.rstrip() for line in fp]

    with open("data/rt_urls.txt", "r") as fp:
        rt_urls = [line.rstrip() for line in fp]

    dark = []
    for url in missing:
        index = rt_urls.index(url)
        identifier = archive_urls[index].replace("https://archive.org/details/", "")
        item = get_item(identifier)
        if item.exists:
            if item.is_dark:
                dark.append(identifier)

    print(f"Found {len(dark):,} dark upload(s) on Internet Archive")

    with open("data/dark.txt", "w") as fp:
        for identifier in dark:
            archive_url = f"https://archive.org/details/{identifier}"
            index = archive_urls.index(archive_url)
            rt_url = rt_urls[index]
            fp.write(f"{archive_url}\t{rt_url}\n")


if __name__ == "__main__":
    identify_dark()
