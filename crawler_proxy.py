import time
import instaloader
import csv
import os
from instaloader.exceptions import ProfileNotExistsException

def configure_proxy(proxy_url):
    """
    Configures the proxy settings for Instaloader using a proxy URL.
    """
    os.environ['http_proxy'] = proxy_url
    os.environ['https_proxy'] = proxy_url

def getboth(posts_info, likesOnPosts, idsOnPosts, time_imported):  # return videos and images (including Reels)
    averageLikes = []
    for post in posts_info:
        if post["media_type"] == "video":  # If it's a video or Reel, use views
            views = post["views"]
            post_time = post["timestamp"].timestamp()

            # Calculate viral based on views
            averageLikes.append(views)  # Collect views for average calculation

            days_since_post = (time.time() - post_time) / (60 * 60 * 24)
            if days_since_post < int(time_imported):
                likesOnPosts.append(views)  # Track views instead of likes
                idsOnPosts.append(post["shortcode"])  # Use shortcode for the post ID
        else:  # For photos, continue using likes
            likes = post["likes"]
            post_time = post["timestamp"].timestamp()

            # Calculate viral based on likes
            averageLikes.append(likes)

            days_since_post = (time.time() - post_time) / (60 * 60 * 24)
            if days_since_post < int(time_imported):
                likesOnPosts.append(likes)
                idsOnPosts.append(post["shortcode"])  # Use shortcode for the post ID

    avgLikes = sum(averageLikes) / len(averageLikes) if averageLikes else 0
    return likesOnPosts, idsOnPosts, avgLikes

def getphotos(posts_info, likesOnPosts, idsOnPosts, time_imported):  # return only photos
    averageLikes = []
    for post in posts_info:
        if post["media_type"] == "photo":  # Only photos
            likes = post["likes"]
            post_time = post["timestamp"].timestamp()

            averageLikes.append(likes)

            days_since_post = (time.time() - post_time) / (60 * 60 * 24)
            if days_since_post < int(time_imported):
                likesOnPosts.append(likes)
                idsOnPosts.append(post["shortcode"])  # Use shortcode for the post ID

    avgLikes = sum(averageLikes) / len(averageLikes) if averageLikes else 0
    return likesOnPosts, idsOnPosts, avgLikes

def getvideos(posts_info, likesOnPosts, idsOnPosts, time_imported):  # return only videos and reels
    averageViews = []
    for post in posts_info:
        if post["media_type"] == "video":  # Only videos or Reels
            views = post["views"]
            post_time = post["timestamp"].timestamp()

            averageViews.append(views)

            days_since_post = (time.time() - post_time) / (60 * 60 * 24)
            if days_since_post < int(time_imported):
                likesOnPosts.append(views)  # Track views instead of likes
                idsOnPosts.append(post["shortcode"])  # Use shortcode for the post ID

    avgViews = sum(averageViews) / len(averageViews) if averageViews else 0
    return likesOnPosts, idsOnPosts, avgViews

def fetch_instagram_data(username):
    """Fetches Instagram profile and post data if the account exists."""
    L = instaloader.Instaloader()

    try:
        # Load the profile
        profile = instaloader.Profile.from_username(L.context, username)
        
        profile_data = {
            "username": profile.username,
            "full_name": profile.full_name,
            "follower_count": profile.followers,
            "following_count": profile.followees,
            "post_count": profile.mediacount,
        }
        
        posts_data = []
        
        # Iterate over profile's posts
        for post in profile.get_posts():
            posts_data.append({
                "likes": post.likes,
                "views": post.video_view_count if post.is_video else None,  # Add view count for videos
                "timestamp": post.date_utc,
                "url": post.url,
                "shortcode": post.shortcode,  # Use shortcode for the post ID
                "media_type": "video" if post.is_video else "photo",  # Treat Reels as videos
                "caption": post.caption  # Include the post caption
            })
            
            # Optionally, limit the number of posts fetched
            if len(posts_data) >= 12:
                break
        
        return profile_data, posts_data

    except ProfileNotExistsException:
        print(f"Error: The Instagram account '{username}' does not exist.")
        return None, None

    except Exception as e:
        print(f"Error fetching data for {username}: {e}")
        return None, None

def find_posts(username, bestposts, time_imported, csv_data):
    """Find viral posts based on views for videos and likes for photos, and time frame."""
    profile_data, posts_info = fetch_instagram_data(username)
    
    if not posts_info:
        return bestposts
    
    likesOnPosts = []
    idsOnPosts = []
    averageLikes = []

    if mediaType == "b":  # If chose both (videos, Reels, and photos)
        likesOnPosts, idsOnPosts, averageLikes = getboth(posts_info, likesOnPosts, idsOnPosts, time_imported)
    elif mediaType == "p":  # Only photos
        likesOnPosts, idsOnPosts, averageLikes = getphotos(posts_info, likesOnPosts, idsOnPosts, time_imported)
    else:  # Only videos and Reels
        likesOnPosts, idsOnPosts, averageLikes = getvideos(posts_info, likesOnPosts, idsOnPosts, time_imported)

    # Determine viral posts
    for idx, post in enumerate(posts_info):
        # Make sure we are within the range of available likes and ids
        if idx >= len(likesOnPosts) or idx >= len(idsOnPosts):
            continue

        viral = False
        viral_score = 0
        post_url = f"https://www.instagram.com/p/{idsOnPosts[idx]}"  # Construct Instagram post URL
        if likesOnPosts[idx] > averageLikes + (0.6 * averageLikes):  # If it's considered a viral post
            viral_score = 1 - (averageLikes / likesOnPosts[idx])  # Viral score
            viral = True
            print(f"{username} : Viral Post Found: {post_url} - Viral Score: {viral_score * 100:.2f}%")
            if viral_score > bestposts[0][1]:  # If score higher than on current list, replace it
                bestposts.pop(0)
                bestposts.append([idsOnPosts[idx], viral_score])
                bestposts.sort(key=lambda x: x[1])
        
        # Add all relevant post information to CSV data, including caption
        csv_data.append([
            profile_data["username"],
            profile_data["full_name"],
            profile_data["follower_count"],
            profile_data["following_count"],
            profile_data["post_count"],
            post["shortcode"],
            post["media_type"],
            post["likes"],
            post["views"] if post["views"] else "N/A",
            post["timestamp"],
            post_url,  # Include post URL
            post["caption"],  # Add caption
            viral,
            viral_score
        ])
    
    return bestposts

def export_to_csv(csv_data, filename="instagram_data.csv"):
    """Exports all post data to a CSV file."""
    headers = [
        "Username", "Full Name", "Follower Count", "Following Count", "Total Posts",
        "Post ID", "Media Type", "Likes", "Views", "Timestamp", "Post URL", "Caption", "Is Viral?", "Viral Score"
    ]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(csv_data)

# Initialize user input
mediaType = ""
time_imported = ""

def run_intro():
    mediaType = "b"
    time_imported = "90"
    if mediaType not in ["v", "b", "p"]:
        print("Error, only type v, b, or p")
    if not time_imported.isdigit():
        print("Error, use only positive numbers for the days.")
    return time_imported, mediaType

# Main execution flow
while mediaType not in ["v", "b", "p"] or not time_imported.isdigit():
    time_imported, mediaType = run_intro()

# Proxy configuration
#proxy_url = "http://username:password@proxyserver:port"  # Replace with your residential proxy details
#configure_proxy(proxy_url)  # Set the proxy configuration for Instaloader

# List of Instagram pages to analyze
pages_to_analyze = "wealth money.focus passionateincome businessideas365 businessmindset101 thebusinesshacks entrepreneurshipfacts businessrealm entrepreneursquote businessaims businessleaderss entrepreneurshipquote businesslogics businessmotivationfamily allaroundbusiness millionaire_lines millionaire_motivator businessgrowthmentor millionaire.dream millionairesformula millionaire_codes success.habits success__tips the.success.club 6amsuccess successowner success.rule fuckmillionsmakebillions moneyforthemind motivationmafia empire_growth minoritymindset billionairesage words_worth_billions rich.quote legendofmotivation incomenotebook incomefact academy_of_wealth businessunions greatness"
pageslist = pages_to_analyze.split(" ")
viralPostData = [["a", 0], ["b", 0], ["c", 0], ["d", 0], ["e", 0], ["f", 0], ["g", 0], ["h", 0], ["i", 0]]  # Empty list to start with
csv_data = []  # List to store all data for CSV export

# Analyze each page for viral content
for user in pageslist:
    profile_data, posts_info = fetch_instagram_data(user)
    if profile_data is None or posts_info is None:
        # Skip this account if it doesn't exist or if there was an error
        continue
    
    viralPostData = find_posts(user, viralPostData, time_imported, csv_data)

# Export data to CSV
export_to_csv(csv_data)
print("Instagram data exported to instagram_data.csv.")
