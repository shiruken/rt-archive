[![Update Rooster Teeth Data](https://github.com/shiruken/rt-archive/actions/workflows/update_rt.yml/badge.svg)](https://github.com/shiruken/rt-archive/actions/workflows/update_rt.yml) [![Update Internet Archive Data](https://github.com/shiruken/rt-archive/actions/workflows/update_archive.yml/badge.svg)](https://github.com/shiruken/rt-archive/actions/workflows/update_archive.yml) [![Identify Dark Uploads](https://github.com/shiruken/rt-archive/actions/workflows/update_archive_dark.yml/badge.svg)](https://github.com/shiruken/rt-archive/actions/workflows/update_archive_dark.yml)

# Rooster Teeth Archive

## Archive Progress Tracker

Track the progress of the ongoing effort to mirror the Rooster Teeth website to Internet Archive.

https://shiruken.github.io/rt-archive/

### Metrics

* Rooster Teeth Videos: 42,592
* Items on Internet Archive: 41,538 (97.53%)
* Items Missing from Internet Archive: 1,051 (2.47%)
* Incomplete Items on Internet Archive: 625
* Items Removed from Internet Archive: 2

## Rooster Teeth API

Comprehensive mirror of the Rooster Teeth API [stored on Internet Archive](https://archive.org/details/roosterteeth-api). The pages of each endpoint are condensed to a single JSON file for easy download.

*Updated every 4 hours on the hour*

### `/watch`

This endpoint lists every video published on the Rooster Teeth website, *including* bonus content.

* Original: https://svod-be.roosterteeth.com/api/v1/watch
* Mirror: https://archive.org/download/roosterteeth-api/api/v1/watch.json (**Warning: Large File**)

### `/episodes`

This endpoint lists every episode published on the Rooster Teeth website, *excluding* bonus content.

* Original: https://svod-be.roosterteeth.com/api/v1/episodes
* Mirror: https://archive.org/download/roosterteeth-api/api/v1/episodes.json (**Warning: Large File**)

### `/shows`

This endpoint lists every show published on the Rooster Teeth website.

*Note: This endpoint is **supposed** to list every show published on the website, however it is missing seven shows that appear in the `/watch` endpoint: Inside Gaming Daily, Inside Gaming Explains, Inside Gaming Features, Inside Gaming Live!, Inside Gaming Podcast, Inside Gaming Reviews, and Inside Gaming Special.*

* Original: https://svod-be.roosterteeth.com/api/v1/shows
* Mirror: https://archive.org/download/roosterteeth-api/api/v1/shows.json

### `/channels`

This endpoint lists every channel published on the Rooster Teeth website.

* Original: https://svod-be.roosterteeth.com/api/v1/channels
* Mirror: https://archive.org/download/roosterteeth-api/api/v1/channels.json

## Derived Files

Listings derived from the Rooster Teeth API and Internet Archive Scrape API. Predominantly for use with the [`rooster`](https://github.com/i3p9/rooster) archival script.

*Updated every hour at minute 30*

* [`missing.txt`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/missing.txt): Rooster Teeth URLs for every video *missing* from Internet Archive (includes 'dark' uploads)
* [`incomplete_urls.csv`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/incomplete_urls.csv): Internet Archive and corresponding Rooster Teeth URLs for every video with an *incomplete* upload to Internet Archive
  * [`incomplete_rt_urls.txt`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/incomplete_rt_urls.txt): Rooster Teeth URLs only
  * [`incomplete_archive_urls.txt`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/incomplete_archive_urls.txt): Internet Archive URLs only

*Updated every 4 hours on the hour*

* [`urls.csv`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/urls.csv): Mapping between Internet Archive URLs and Rooster Teeth URLs for every video
  * [`rt_urls.txt`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/rt_urls.txt): Rooster Teeth URLs only
  * [`archive_urls.txt`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/archive_urls.txt): Internet Archive URLs only
* [`shows.csv`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/shows.csv): Mapping between show titles and URL slugs
* [`checklist.csv`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/checklist.csv): Data formatted for the [RT Archival Checklist](https://docs.google.com/spreadsheets/d/17Vqd_xYLh-xma_nw_TkeFexzQ2sZ4uEntibiZB8KlRI/preview)

*Updated daily at 00:45*

* [`dark.csv`](https://raw.githubusercontent.com/shiruken/rt-archive/main/data/dark.csv): URLs for every upload *removed* (i.e. made dark) by Internet Archive.
