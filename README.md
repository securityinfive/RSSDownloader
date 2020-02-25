# RSSDownloader
Download all the current MP3s from your favorite podcast RSS feed.

This little app started off as an exercise as I teach myself Python and grew into this. This will take an RSS feed of a podcast, ask you how many of the latest episodes you want to download locally and then download the mp3s. 

In the Python file you will need to provive the following two items
   - RSS_Target = "http of the RSS Feed"
   - local_target_dir = "local directory to download to"
  
  Example:
    - RSS_Target = "https://securityinfive.libsyn.com/securityinfive/rss
    - local_target_dir = "C:\Dev\PodcastDownloads\SecurityInFive"
    
When you run the script you will be asked how many to download, enter a number or 0 for all of the avialable episodes.
The script will skip episodes that already exist in the target directory.

That's it.
