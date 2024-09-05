
# Instagram Viral Post Finder Tool

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [How It Works](#how-it-works)
4. [Viral Detection Algorithm](#viral-detection-algorithm)
5. [Installation](#installation)
6. [Using the Tool](#using-the-tool)
7. [Examples](#examples)
8. [Proxy Configuration](#proxy-configuration)
9. [Output](#output)
10. [Technical Details](#technical-details)

## Introduction

The **Instagram Viral Post Finder Tool** is a Python-based application designed to help users identify viral posts on Instagram. This tool scrapes Instagram profiles, retrieves engagement metrics such as likes and views, and determines which posts can be classified as viral based on an algorithm that compares post engagement against the average performance.

The tool also includes the ability to use **residential rotating proxies**, making it suitable for users who need to bypass Instagram rate limits or geographic restrictions.

## Features

- **Scrapes Instagram Profiles**: Collects profile information, including follower count, following count, and the most recent posts (up to 12).
- **Viral Post Detection**: Uses an algorithm to identify viral posts based on likes (for photos) or views (for videos).
- **Captures Post Metadata**: Extracts the caption, post URL, timestamp, and engagement metrics for each post.
- **Proxy Support**: Routes traffic through residential rotating proxies to avoid rate limits.
- **CSV Export**: Outputs all data into a CSV file for easy analysis, including the viral status of each post.

## How It Works

The tool uses the `Instaloader` Python library to connect to Instagram, retrieve profile and post data, and then apply a viral detection algorithm to assess each post's performance.

### Steps Overview:

1. **Proxy Setup**: If using a proxy (optional), the tool can be configured to route all HTTP requests through the proxy.
2. **Profile Scraping**: The tool fetches basic profile details, such as the number of followers and the total number of posts.
3. **Post Scraping**: The most recent 12 posts (configurable) are scraped for engagement data (likes for photos, views for videos).
4. **Viral Post Analysis**: The tool applies an algorithm to compare each post’s engagement to the average engagement across all posts. Posts that exceed a threshold are flagged as viral.
5. **CSV Export**: All scraped data, including viral detection results, are saved in a CSV file for further analysis.

## Viral Detection Algorithm

The core functionality of this tool is its ability to detect viral posts. It does this by comparing each post's engagement (likes/views) to the average engagement of the user’s recent posts.

### Steps in the Viral Detection Process:

1. **Fetch Engagement Metrics**:
   - For photos: Extract the number of likes.
   - For videos: Extract the number of views.

2. **Calculate Average Engagement**:
   - The tool calculates the average engagement across all fetched posts. 
   ```
   Average Engagement = Total Engagement / Number of Posts
   ```

3. **Determine Viral Threshold**:
   - A post is considered viral if its engagement exceeds **60% above the average**:
   ```
   Viral Threshold = Average Engagement + (0.6 * Average Engagement)
   ```

4. **Viral Score Calculation**:
   - If a post exceeds the viral threshold, it is flagged as viral. Additionally, a viral score is calculated to determine how much more viral the post is compared to the average:
   ```
   Viral Score = 1 - (Average Engagement / Post Engagement)
   ```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/instagram-viral-finder.git
cd instagram-viral-finder
```

### 2. Install Required Python Packages
You need to install `Instaloader` for scraping Instagram data:
```bash
pip install instaloader
```

## Using the Tool

### 1. Configuring Proxies (Optional)
If you want to use a residential rotating proxy, set your proxy details in the script by replacing `proxy_url` with your proxy service credentials:
```python
proxy_url = "http://username:password@proxyserver:port"  # Replace with your proxy details
configure_proxy(proxy_url)
```

### 2. Running the Script
To run the tool and scrape profiles for viral post analysis, execute the script:

Info: Welche Instagram Account sind in der Python File definiert:

Läd mit Instaloader Python die Profile und speichert sie in einer CSV Datei.
```bash
python crawler_proxy_file.py
```

Läd mit Instaloader die Profile und speichert die Daten in JSON Dateien.
```bash
python crawler_proxy_download.py
```

### 3. Setting Instagram Accounts to Analyze
In the script, you can specify the list of Instagram usernames to analyze:
```python
pages_to_analyze = "wealth money.focus passionateincome"
```
This will analyze the specified profiles and detect viral posts for each one.

### 4. CSV Output
The tool exports the results into a CSV file named `instagram_data.csv`, which includes all post data, engagement metrics, viral status, and more.

## Examples

### Example 1: Detecting Viral Photos

Let’s say the average number of likes for an Instagram user’s posts is **100 likes**. If one of the user’s posts has **180 likes**, the tool will classify this post as viral because:

1. **Average Likes** = 100
2. **Viral Threshold** = 100 + (0.6 * 100) = 160
3. Since **180 likes** > **160 likes**, the post is flagged as **viral**.

- **Viral Score**:
   ```
   Viral Score = 1 - (100 / 180) = 0.44
   ```

This score indicates that the post’s engagement is 44% higher than the average.

### Example 2: Detecting Viral Videos

Suppose the tool analyzes a video post with **2000 views**, and the average views across other videos from this user are **1200 views**.

1. **Average Views** = 1200
2. **Viral Threshold** = 1200 + (0.6 * 1200) = 1920
3. Since **2000 views** > **1920 views**, the post is flagged as **viral**.

- **Viral Score**:
   ```
   Viral Score = 1 - (1200 / 2000) = 0.40
   ```

This score means the video post received 40% more views than the average.

## Proxy Configuration

### Why Use Proxies?
Instagram often limits the number of requests a single IP address can make, especially if the requests are frequent. Using residential rotating proxies allows you to bypass these rate limits by rotating IP addresses for each request.

### How to Configure a Proxy:
1. Set the proxy URL in the script:
   ```python
   proxy_url = "http://username:password@proxyserver:port"  # Replace with actual proxy details
   configure_proxy(proxy_url)
   ```

2. Ensure the proxy supports **HTTP/HTTPS** requests, and provide any required authentication details (username and password) in the proxy URL.

3. Once configured, the tool will route all traffic through the proxy.

## Output

The tool exports all scraped data into a CSV file (`instagram_data.csv`), which includes the following columns:

| Column Name       | Description                                      |
|-------------------|--------------------------------------------------|
| **Username**       | Instagram username of the profile                |
| **Full Name**      | Full name of the user                            |
| **Follower Count** | Total number of followers                        |
| **Following Count**| Total number of accounts the user is following   |
| **Total Posts**    | Total number of posts on the profile             |
| **Post ID**        | Unique ID of the Instagram post                  |
| **Media Type**     | Type of post (photo or video)                    |
| **Likes**          | Number of likes (for photos)                     |
| **Views**          | Number of views (for videos)                     |
| **Timestamp**      | Date and time when the post was published        |
| **Post URL**       | Direct URL to the Instagram post                 |
| **Caption**        | Caption text of the post                         |
| **Is Viral?**      | Indicates if the post is viral (`True/False`)    |
| **Viral Score**    | Viral score indicating how viral the post is     |

## Technical Details

1. **Instaloader**: The tool uses the `Instaloader` Python library to scrape Instagram profiles and fetch metadata such as likes, views, captions, and timestamps.
2. **Proxy Support**: Proxies are implemented using Python's standard `os.environ` settings for `http_proxy` and `https_proxy`.
3. **Viral Algorithm**: The viral detection algorithm calculates a threshold for engagement and flags posts that exceed this threshold by 60% or more.
