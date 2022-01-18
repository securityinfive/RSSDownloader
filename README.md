# RSSDownloader
Download all the current MP3s from your favorite podcast RSS feed.


Usage:

>    python3 RSSDownloader.py RSS_Feed [Max_Items] [Local_Folder] [--Title]

This will take an RSS feed of a podcast, to download locally and then download the mp3s.

A Maximum Limit, Max_Items, can be provided, otherwise all files are downloaded.

A download location, Local_Folder, can be provided, if not provided stored in the current directory.

If --Title, or -T, is provides, then the file is downloaded with the name of the episode.

The script will skip episodes that already exist in the target directory.

That's it.

python3 is required


## Known Issues:

*  Only downloads mp3 files
*  If the download it interrupted then a partial file remains, which is a limitation of wget.py
