<img src="http://www.nicolaspettican.com/css/img/instabot.png" title="Instabot logo" alt="Instabot logo" width="30%">

# SMARTEE
Social Media Automated Research Tool to Evaluate Engagement

## In a nutshell

### You can

- [x] Track posts that mention specific hashtags
- [x] Identify influencers
- [x] Identify company brand ambassadors

### Your input

* A list of hashtags
* A list of hashtags to avoid (optional)
* A list of users to track (optional)

### The output

An Excel file with:

* A line graph showing the spread of posts throughout the tracking time
* A list of posts organised by author showing:
  - Likes
  - Comments
  - Followers
  - Following
  - Popularity
  - Hashtags
  - Caption
  - And more
* A table with the number of posts for the hashtag per day

The output also comes as JSON, so if you are interested in this let me know in the issues section.

## Getting started

The purpose of SMARTEE is to **track Instagram posts** that include certain **hashtags** as they are published, and **identify influencers and engagers**. It is also a great tool to measure how engaged employees are with the company hashtag and who is the biggest company brand ambassador.

### Prerequisites

Python 2.7 and a server. 

A Raspberry Pi is great for this (maybe you have one lying around without a purpose).

### Installing

1. Download a copy of the repo or clone to your preferred directory
2. Fill out the config file with your parameters and execute the `run.py` file

> More explanation to come
