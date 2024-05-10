[![Update Rooster Teeth Data](https://github.com/shiruken/rt-archive/actions/workflows/update_rt.yml/badge.svg)](https://github.com/shiruken/rt-archive/actions/workflows/update_rt.yml) [![Update Internet Archive Data](https://github.com/shiruken/rt-archive/actions/workflows/update_archive.yml/badge.svg)](https://github.com/shiruken/rt-archive/actions/workflows/update_archive.yml) [![Identify Dark Uploads](https://github.com/shiruken/rt-archive/actions/workflows/update_archive_dark.yml/badge.svg)](https://github.com/shiruken/rt-archive/actions/workflows/update_archive_dark.yml)

# Rooster Teeth Archive

## Archive Progress Tracker

Track the progress of the ongoing effort to mirror the Rooster Teeth website to Internet Archive.

https://shiruken.github.io/rt-archive/

### Metrics

* Rooster Teeth Videos: 42,603
* Items on Internet Archive: 42,602 (100.00%)
* Items Missing from Internet Archive: 2 (0.00%)
* Incomplete Items on Internet Archive: 852
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

## Rooster Teeth API Images

Comprehensive mirror of the images referenced in the Rooster Teeth API [stored on Internet Archive](https://archive.org/details/roosterteeth-api-images). The archived images can be accessed by swapping the original domain name with the Internet Archive download URL:

`cdn.roosterteeth.com` → `archive.org/download/roosterteeth-api-images`

* Original: https://cdn.roosterteeth.com/image/upload/t_l/f_auto/3/9a671db3-c156-4085-9629-428a81ce26e7/original/1634598688.jpg
* Mirror: https://archive.org/download/roosterteeth-api-images/image/upload/t_l/f_auto/3/9a671db3-c156-4085-9629-428a81ce26e7/original/1634598688.jpg

A small number of images (12) were stored using a bare AWS domain. These should be mapped with:

`s3.amazonaws.com/dev.cdn.roosterteeth.com` → `archive.org/download/roosterteeth-api-images/image`

* Original: https://s3.amazonaws.com/dev.cdn.roosterteeth.com/uploads/images/71044483-a611-4bbf-8c67-724ea09c1f05/original/ep11690.jpg
* Mirror: https://archive.org/download/roosterteeth-api-images/image/uploads/images/71044483-a611-4bbf-8c67-724ea09c1f05/original/ep11690.jpg

There were 2,720,688 image urls referenced by the Rooster Teeth API of which 181,180 were unique. There were 40 broken image links (HTTP Error 404) that could not be archived. They are listed below:

<details>
  <summary>Broken URLs</summary>

  ```bash
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/4bc2aac0-9528-4111-a876-ada9c0efdfa6/original/24363-1437848352684-mirror%27s_edge_catalyst.jpg
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/4bc2aac0-9528-4111-a876-ada9c0efdfa6/original/24363-1437848352684-mirror%27s_edge_catalyst.jpg
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/4bc2aac0-9528-4111-a876-ada9c0efdfa6/original/24363-1437848352684-mirror%27s_edge_catalyst.jpg
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/4bc2aac0-9528-4111-a876-ada9c0efdfa6/original/24363-1437848352684-mirror%27s_edge_catalyst.jpg
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/3b5e7ff2-440a-4416-8cab-30aad0919d40/original/DBZ_Earth%27s_Special_Forces.jpg
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/3b5e7ff2-440a-4416-8cab-30aad0919d40/original/DBZ_Earth%27s_Special_Forces.jpg
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/3b5e7ff2-440a-4416-8cab-30aad0919d40/original/DBZ_Earth%27s_Special_Forces.jpg
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/3b5e7ff2-440a-4416-8cab-30aad0919d40/original/DBZ_Earth%27s_Special_Forces.jpg
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/87749a8f-b5c2-4f1c-b9ed-f9cac2908e1b/original/Reggie-Fils-Aime%27s-ABC-Interview.jpg
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/87749a8f-b5c2-4f1c-b9ed-f9cac2908e1b/original/Reggie-Fils-Aime%27s-ABC-Interview.jpg
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/87749a8f-b5c2-4f1c-b9ed-f9cac2908e1b/original/Reggie-Fils-Aime%27s-ABC-Interview.jpg
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/87749a8f-b5c2-4f1c-b9ed-f9cac2908e1b/original/Reggie-Fils-Aime%27s-ABC-Interview.jpg
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/f9da9a7d-8725-43a3-b007-18d17520f2ae/original/Whomp%27Em.gif
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/f9da9a7d-8725-43a3-b007-18d17520f2ae/original/Whomp%27Em.gif
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/f9da9a7d-8725-43a3-b007-18d17520f2ae/original/Whomp%27Em.gif
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/f9da9a7d-8725-43a3-b007-18d17520f2ae/original/Whomp%27Em.gif
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/40e55b47-a5b0-4ac6-bf84-e07f227cb07f/original/Ghosts_%27N_Goblins_-_NES_-_Title.png
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/40e55b47-a5b0-4ac6-bf84-e07f227cb07f/original/Ghosts_%27N_Goblins_-_NES_-_Title.png
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/40e55b47-a5b0-4ac6-bf84-e07f227cb07f/original/Ghosts_%27N_Goblins_-_NES_-_Title.png
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/40e55b47-a5b0-4ac6-bf84-e07f227cb07f/original/Ghosts_%27N_Goblins_-_NES_-_Title.png
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/3be9bf4a-686d-4402-aa76-b43eb1a3e3d8/original/03+Sonic+The+Hedgehog+2.jpg
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/3be9bf4a-686d-4402-aa76-b43eb1a3e3d8/original/03+Sonic+The+Hedgehog+2.jpg
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/3be9bf4a-686d-4402-aa76-b43eb1a3e3d8/original/03+Sonic+The+Hedgehog+2.jpg
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/3be9bf4a-686d-4402-aa76-b43eb1a3e3d8/original/03+Sonic+The+Hedgehog+2.jpg
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/d3ad1342-7a92-482f-b23a-cc6c23911553/original/01+Sonic+The+Hedgehog+1.jpg
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/d3ad1342-7a92-482f-b23a-cc6c23911553/original/01+Sonic+The+Hedgehog+1.jpg
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/d3ad1342-7a92-482f-b23a-cc6c23911553/original/01+Sonic+The+Hedgehog+1.jpg
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/d3ad1342-7a92-482f-b23a-cc6c23911553/original/01+Sonic+The+Hedgehog+1.jpg
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/13003ad2-3bb3-41f4-9897-6779feefcae2/original/Battleship+(U)+[!]+0.jpg
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/13003ad2-3bb3-41f4-9897-6779feefcae2/original/Battleship+(U)+[!]+0.jpg
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/13003ad2-3bb3-41f4-9897-6779feefcae2/original/Battleship+(U)+[!]+0.jpg
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/13003ad2-3bb3-41f4-9897-6779feefcae2/original/Battleship+(U)+[!]+0.jpg
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/9269b55a-af01-4102-af80-16e97aded6d5/original/Track+and+Field+2.jpg
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/9269b55a-af01-4102-af80-16e97aded6d5/original/Track+and+Field+2.jpg
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/9269b55a-af01-4102-af80-16e97aded6d5/original/Track+and+Field+2.jpg
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/9269b55a-af01-4102-af80-16e97aded6d5/original/Track+and+Field+2.jpg
  https://cdn.roosterteeth.com/image/upload/t_t/f_auto/2/uploads/images/76fd2fe3-ed5b-4ab3-bbca-6f32b480a8e1/original/600full-chip-%27n-dale-rescue-rangers-screenshot.jpg
  https://cdn.roosterteeth.com/image/upload/t_sm/f_auto/2/uploads/images/76fd2fe3-ed5b-4ab3-bbca-6f32b480a8e1/original/600full-chip-%27n-dale-rescue-rangers-screenshot.jpg
  https://cdn.roosterteeth.com/image/upload/t_m/f_auto/2/uploads/images/76fd2fe3-ed5b-4ab3-bbca-6f32b480a8e1/original/600full-chip-%27n-dale-rescue-rangers-screenshot.jpg
  https://cdn.roosterteeth.com/image/upload/t_l/f_auto/2/uploads/images/76fd2fe3-ed5b-4ab3-bbca-6f32b480a8e1/original/600full-chip-%27n-dale-rescue-rangers-screenshot.jpg
  ```
  
</details>

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
