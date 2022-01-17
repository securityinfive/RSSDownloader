"""
Author : Security In Five - https://securityinfive.com
Contact: bblogger@protonmail.com
Source: https://github.com/securityinfive/RSSDownloader

Python script to download MP3 files from a podcast's RSS feed.
Usage:
   - Simply enter the URL for the RSS feed.
   - Enter a local directory where the mp3 files will download to.
   - Run and enter the number of files you want to download from the feed.
        - Specific number within the range of the episodes/files in the feed.
        - Enter 0 and it will download all the files in the feed.

I created this as I teach myself Python on the side. It started off as a simple downloader exercise and I grew
it into a tool for me to archive the 700+ episodes of my podcast from my host. I then expanded it to try
to be dynamic enough to work with any 'standard' RSS feed. Currently the RSS_Target and local_target_dir are hard coded.

Future ideas to change this to where it could be scheduled for regular local downloads outside podcast player services.
"""
import wget
import feedparser
import glob
import os
import argparse
from pprint import pprint
import re

def Get_Feed(rss_to_load):
    # Load the RSS Feed
    print("Getting feed - " + rss_to_load + " please wait...")
    rss_feed_load = feedparser.parse(rss_to_load)
    rss_length = len(rss_feed_load.entries)
    print(f"Feed loaded, {rss_length} items.")

    # Pass back a list
    return rss_feed_load, rss_length

def Download_Files(target_dir, rss_feed, how_many_to_get,rename_to_title):
    # Initialize the download counter
    episode_count = 1
    # Get all the mp3 files in the target directory to skip over existing files and put in a list.
    # Get all the mp3 files in the target directory and load it into a list
    os.chdir(target_dir)
    current_files = []
    for file in glob.glob("*.mp3"):
        current_files.append(file)

    # FOR LOOP THROUGH EPISODES IN FEED
    for episode in rss_feed.entries:
#        pprint(episode)
        entry_links = episode.links
        # second entry for the mp3 link
        # .links has the download in the second entry
        mp3_link = entry_links[1]
        mp3_href = mp3_link['href']

        # Strip out the mp3 file from the download URL for directory search
        # Break out the / directories from the URL
        temp_mp3_link = mp3_href.split('/')
        # Get the count of the URL items, then get position of the mp3 file,
        # the mp3 file will be the last entry http://example.com/epsiode/whatever/something/episode_111.mp3
        temp_mp3_link_last = len(temp_mp3_link) - 1    # minus one because of the array numbering
        # MP3 filename
        temp_mp3_link = temp_mp3_link[temp_mp3_link_last]

        # Make sure the last entry is a .mp3 file
        if ".mp3" in temp_mp3_link:
            # Check to see if there are headers on the URL after .mp3, break them out to get the .mp3 file name
            # Example: http://example.com/epsiode/whatever/something/episode_111.mp3?redirect=1&name=something&where=9
            # If there is no ?, the var is already set to the proper mp3 filename.
            if "?" in temp_mp3_link:
                temp_mp3_link = temp_mp3_link.split("?")
                # Grab the first item, the second will be the headers
                temp_mp3_link = temp_mp3_link[0]

        if rename_to_title:
            if "title" in episode:
                temp_mp3_link = re.sub(r'[<>:/\|?*"]+',"",episode["title"]+".mp3")

                # The sub is to get rid of characters that Windows might not like


        # See if the mp3 file already exists in the target directory for download
        # If yes, skip it. If not, download it.
        if temp_mp3_link in current_files:
            print("File Exists - SKIPPING DOWNLOAD - " + temp_mp3_link)
        else:
            print("Downloading - " + str(temp_mp3_link))

            if rename_to_title:
                if "title" in episode:
                    wget.download(mp3_link['href'], target_dir+"/"+re.sub(r'[<>:/\|?*"]+',"",episode["title"]+".mp3"))
                else:
                    wget.download(mp3_link['href'], target_dir)
            else:
                wget.download(mp3_link['href'], target_dir)
            print(" Downloaded")

        # Iterate the entered count, break out when hit the entered file count
        # If How_Many is 0 the For loop will run to the end.
        if int(how_many_to_get) > 0:
            if str(episode_count) == str(how_many_to_get):
                print("--- DOWNLOAD COMPLETE ---")
                break
            else:
                episode_count = episode_count + 1
    # --- END FOR ---

    # Kick out Complete message when done with all episodes when input is 0
    if int(how_many_to_get) == 0:
        print("--- DOWNLOAD COMPLETE ---")
# -----------------------------------------------------------------------


def get_args():

   parser = argparse.ArgumentParser(fromfile_prefix_chars="@",description='RSS File Downloader', epilog="V1.0", formatter_class=argparse.ArgumentDefaultsHelpFormatter);
   parser.add_argument("RSS_Feed", help="Remote Host",)
   parser.add_argument("Max_Items", help="Max Number of Items",type=int, default=0,  nargs="?")
   parser.add_argument("Local_Folder", help="Local Directory to save the files",type=str, nargs="?",default=".")
   parser.add_argument("--Title", "-T", help="Rename File to episode Title",action="store_true")
   parser = parser.parse_args()
   if parser.Max_Items <0:
      sys.exit("Max_Items must be >= 0")


   return (vars(parser))



def main():
    # Get Started, Load the RSS and break out the feed and file count from the feed
    args=get_args()
    RSS_Target = args["RSS_Feed"]
    local_target_dir = args["Local_Folder"]
    How_Many=args["Max_Items"]

    RSS_Feed = Get_Feed(RSS_Target)
    RSS_Feed_Items = RSS_Feed[0]
    validate_input = RSS_Feed[1]


    # User input for number of files to download and make sure user input is clean
    is_valid = 1

    if int(How_Many) == 0:
        File_Count = "All files to - "
    elif int(How_Many) == 1:
        File_Count = str(How_Many) + " file to - "
    else:
        File_Count = str(How_Many) + " files to - "
    print("Downloading " + File_Count + local_target_dir)
    Download_Files(local_target_dir, RSS_Feed_Items, How_Many,args["Title"])

    # End Of Line


if __name__ == '__main__':
    main()
