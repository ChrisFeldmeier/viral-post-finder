import time
import instaloader
import csv
import os
import subprocess
from datetime import datetime, timedelta
from instaloader.exceptions import ProfileNotExistsException

def configure_proxy(proxy_url):
    """
    Configures the proxy settings for Instaloader using a proxy URL.
    """
    os.environ['http_proxy'] = proxy_url
    os.environ['https_proxy'] = proxy_url

def save_profile_metadata_json(username):
    """
    Save Instagram profile metadata as a JSON file using Instaloader command-line tool.
    """
    try:
        # Use Instaloader command-line to save metadata as JSON without downloading pictures
        subprocess.run(["instaloader",
                        "--no-pictures",
                        "--no-videos",
                        "--no-profile-pic",
                        "--no-video-thumbnails",
                        "--no-compress-json",
                        "profile", username], check=True)
        print(f"Profile metadata for {username} downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading profile metadata for {username}: {e}")

def save_post_metadata_json(username):
    """
    Save Instagram post metadata as JSON files using Instaloader command-line tool.
    """
    try:
        # Use Instaloader command-line to save metadata for all posts without downloading pictures
        #subprocess.run([
        #     "instaloader", 
        #     "--metadata-json", 
        #     "--no-pictures", 
        #     "--dirname-pattern={profile}", 
        #    "--filename-pattern={profile}_{shortcode}", 
        #    "profile", username
        #], check=True)
        print(f"Post metadata for {username} downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading post metadata for {username}: {e}")


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
def getphotos(posts_info, likesOnPosts, idsOnPosts, time_imported):  
    """Return only photos from the posts data."""
    averageLikes = []
    for post in posts_info:
        if post["media_type"] == "photo":  # Only process photos
            likes = post["likes"]
            post_time = post["timestamp"].timestamp()

            # Calculate likes and append them
            averageLikes.append(likes)

            days_since_post = (time.time() - post_time) / (60 * 60 * 24)
            if days_since_post < int(time_imported):
                likesOnPosts.append(likes)
                idsOnPosts.append(post["shortcode"])  # Use shortcode for the post ID

    avgLikes = sum(averageLikes) / len(averageLikes) if averageLikes else 0
    return likesOnPosts, idsOnPosts, avgLikes

def getvideos(posts_info, likesOnPosts, idsOnPosts, time_imported):  
    """Return only videos and reels from the posts data."""
    averageViews = []
    for post in posts_info:
        if post["media_type"] == "video":  # Only process videos or Reels
            views = post["views"]
            post_time = post["timestamp"].timestamp()

            # Calculate views and append them
            averageViews.append(views)

            days_since_post = (time.time() - post_time) / (60 * 60 * 24)
            if days_since_post < int(time_imported):
                likesOnPosts.append(views)  # Track views instead of likes
                idsOnPosts.append(post["shortcode"])  # Use shortcode for the post ID

    avgViews = sum(averageViews) / len(averageViews) if averageViews else 0
    return likesOnPosts, idsOnPosts, avgViews

def fetch_instagram_data(username, L):
    """Fetches Instagram profile and post data if the account exists."""
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

        # Save profile metadata using CLI
        #save_profile_metadata_json(username)
        
        posts_data = []
        for post in profile.get_posts():
            # Save post metadata using CLI
            #save_post_metadata_json(username)

            posts_data.append({
                "likes": post.likes,
                "views": post.video_view_count if post.is_video else None,  # Add view count for videos
                "timestamp": post.date_utc,
                "url": post.url,
                "shortcode": post.shortcode,  # Use shortcode for the post ID
                "media_type": "video" if post.is_video else "photo",  # Treat Reels as videos
                "caption": post.caption,  # Include the post caption,
                "media_id": post.mediaid,  # Include the post media URL
                "media_url": post.video_url if post.is_video else post.url,
                "comments": post.comments,
                "tagged_users": post.tagged_users,
                "caption_mentions": post.caption_mentions,
                "caption_hashtags": post.caption_hashtags,
                "location": post.location,
                "typename": post.typename,
                "owner_username": post.owner_username
            })
            
            if len(posts_data) >= 12:  # Limit to 12 posts
                break
        
        return profile_data, posts_data

    except ProfileNotExistsException:
        print(f"Error: The Instagram account '{username}' does not exist.")
        return None, None

    except Exception as e:
        print(f"Error fetching data for {username}: {e}")
        return None, None

def calculate_engagement_rate(posts_data, follower_count):
    """Calculates the engagement rate based on the last 16 images."""
    total_likes = sum(post['likes'] for post in posts_data)
    total_comments = sum(post.get('comments', 0) for post in posts_data)
    engagement_rate = (total_likes + total_comments) / (follower_count * len(posts_data)) * 100
    avg_likes = total_likes / len(posts_data)
    avg_comments = total_comments / len(posts_data) if total_comments else 0
    return engagement_rate, avg_likes, avg_comments

def find_posts(username, bestposts, time_imported, csv_data, L):
    """Find viral posts based on views for videos and likes for photos, and time frame."""
    profile_data, posts_info = fetch_instagram_data(username, L)
    
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

    # Calculate engagement rate, avg likes, avg comments
    engagement_rate, avg_likes, avg_comments = calculate_engagement_rate(posts_info, profile_data['follower_count'])

    # Determine viral posts
    for idx, post in enumerate(posts_info):
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
            viral_score,
            engagement_rate,
            avg_likes,
            avg_comments,
            post["media_id"],
            post["media_url"],
            post["comments"],
            post["tagged_users"],
            post["caption_mentions"],
            post["caption_hashtags"],
            post["location"],
            post["typename"],
            post["owner_username"]
            ])
    
    return bestposts

def export_to_csv(csv_data, filename="instagram_data.csv"):
    """Exports all post data to a CSV file."""
    headers = [
        "Username", "Full Name", "Follower Count", "Following Count", "Total Posts",
        "Post ID", "Media Type", "Likes", "Views", "Timestamp", "Post URL", "Caption", "Is Viral?", 
        "Viral Score", "Engagement Rate", "Avg Likes", "Avg Comments",
        "Media ID", "Media URL", "Comments", "Tagged Users", "Caption Mentions", "Caption Hashtags", "Location", "Typename", "Owner Username"
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
proxy_url = "https://spww9ibbim:1Kuw7E3x0+beEltaIi@gate.smartproxy.com:10001"  # Replace with your residential proxy details
configure_proxy(proxy_url)  # Set the proxy configuration for Instaloader

# Create an instance of Instaloader
L = instaloader.Instaloader()

# List of Instagram pages to analyze
pages_to_analyze = "wealth money.focus passionateincome"
pageslist = pages_to_analyze.split(" ")

viralPostData = [["a", 0]] * 9  # Initialize with dummy data
csv_data = []  # List to store all data for CSV export

# Analyze each page for viral content
for user in pageslist:
    viralPostData = find_posts(user, viralPostData, time_imported, csv_data, L)

# Export data to CSV
export_to_csv(csv_data)
print("Instagram data exported to instagram_data.csv.")