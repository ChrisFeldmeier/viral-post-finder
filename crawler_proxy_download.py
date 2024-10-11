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
        #subprocess.run(["instaloader",
        #                "--no-pictures",
        #                "--no-videos",
        #                "--no-profile-pic",
        #                 "--no-video-thumbnails",
        #                "--no-compress-json",
         #               "profile", username], check=True)
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

def fetch_instagram_data(username, L, retries=10):
    """Fetches Instagram profile and post data if the account exists, with retry logic."""
    attempt = 0
    while attempt < retries:
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
            post_count = 0
            
            # Loop through posts with retry for each post fetch
            for post in profile.get_posts():
                post_attempt = 0
                while post_attempt < retries:
                    try:
                        if post_count >= 12:
                            break
                        
                        post_data = {
                            "likes": post.likes if hasattr(post, 'likes') else None,
                            "views": post.video_view_count if post.is_video and hasattr(post, 'video_view_count') else None,
                            "timestamp": post.date_utc if hasattr(post, 'date_utc') else None,
                            "url": post.url if hasattr(post, 'url') else None,
                            "shortcode": post.shortcode if hasattr(post, 'shortcode') else None,
                            "media_type": "video" if post.is_video else "photo",
                            "caption": post.caption if hasattr(post, 'caption') else None,
                            "media_id": post.mediaid if hasattr(post, 'mediaid') else None,
                            "media_url": post.video_url if post.is_video and hasattr(post, 'video_url') else (post.url if hasattr(post, 'url') else None),
                            "comments": post.comments if hasattr(post, 'comments') else None,
                            "tagged_users": post.tagged_users if hasattr(post, 'tagged_users') else None,
                            "caption_mentions": post.caption_mentions if hasattr(post, 'caption_mentions') else None,
                            "caption_hashtags": post.caption_hashtags if hasattr(post, 'caption_hashtags') else None,
                            "location": post.location if hasattr(post, 'location') else None,
                            "typename": post.typename if hasattr(post, 'typename') else None,
                            "owner_username": post.owner_username if hasattr(post, 'owner_username') else None,
                            "is_sponsored": post.is_sponsored if hasattr(post, 'is_sponsored') else None,
                            "video_duration": post.video_duration if post.is_video and hasattr(post, 'video_duration') else None,
                            "is_video": post.is_video if hasattr(post, 'is_video') else None,
                            "is_pinned": post.is_pinned if hasattr(post, 'is_pinned') else None,
                            "has_audio": post._iphone_struct_.get("has_audio", "") if hasattr(post, '_iphone_struct_') else None,
                            "sponsor_users": post.sponsor_users if hasattr(post, 'sponsor_users') else None,
                            "ad_id": post._iphone_struct_.get("ad_id", "") if hasattr(post, '_iphone_struct_') else None,
                            "is_paid_partnership": post._iphone_struct_.get("is_paid_partnership", "") if hasattr(post, '_iphone_struct_') else None,
                            "boosted_status": post._iphone_struct_.get("boosted_status", "") if hasattr(post, '_iphone_struct_') else None,
                            "like_and_view_counts_disabled": post._iphone_struct_.get("like_and_view_counts_disabled", "") if hasattr(post, '_iphone_struct_') else None,
                            "link": post._iphone_struct_.get("link", "") if hasattr(post, '_iphone_struct_') else None,
                            "full_metadata": post._full_metadata if hasattr(post, '_full_metadata') else None,
                        }
                        
                        print(f"{post.owner_username} - https://www.instagram.com/p/{post.shortcode} ")  # Print the post data
                        posts_data.append(post_data)
                        post_count += 1
                        break  # Exit retry loop if post fetch was successful
                    except Exception as post_e:
                        print(f"Error fetching post for {username}: {post_e}. Retrying post {post_attempt + 1}/{retries}...")
                        post_attempt += 1
                        time.sleep(3)  # Wait before retrying
                if post_attempt == retries:
                    print(f"Failed to fetch post for {username} after {retries} attempts.")
            
            return profile_data, posts_data

        except ProfileNotExistsException:
            print(f"Error: The Instagram account '{username}' does not exist.")
            return None, None

        except Exception as e:
            print(f"Error fetching data for {username}: {e}. Retrying {attempt + 1}/{retries}...")
            attempt += 1
            time.sleep(5)  # Wait before retrying

    print(f"Failed to fetch data for {username} after {retries} attempts.")
    return None, None


def calculate_engagement_rate(posts_data, follower_count):
    """Calculates the engagement rate based on the last 16 images."""
    total_likes = sum(post['likes'] for post in posts_data)
    total_comments = sum(post.get('comments', 0) for post in posts_data)
    engagement_rate = (total_likes + total_comments) / (follower_count * len(posts_data)) * 100
    avg_likes = total_likes / len(posts_data)
    avg_comments = total_comments / len(posts_data) if total_comments else 0
    return engagement_rate, avg_likes, avg_comments

def find_posts(username, bestposts, time_imported, csv_data, L, retries=10):
    """Find viral posts based on views for videos and likes for photos, and time frame."""
    profile_data, posts_info = fetch_instagram_data(username, L, retries)
    
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

    # Limit to the first 12 posts
    posts_info = posts_info[:12]
    likesOnPosts = likesOnPosts[:12]
    idsOnPosts = idsOnPosts[:12]

    # Determine viral posts
    for idx, post in enumerate(posts_info):
        try:
            viral = False
            viral_score = 0
            post_url = f"https://www.instagram.com/p/{idsOnPosts[idx]}"  # Construct Instagram post URL

            if likesOnPosts[idx] > averageLikes + (0.6 * averageLikes):  # If it's considered a viral post
                viral_score = (likesOnPosts[idx] / averageLikes) - 1  # Viral score as a positive ratio
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
                post["likes"],
                post["views"] if post["views"] else "N/A",
                post["timestamp"],
                post_url,  # Include post URL
                post["shortcode"],
                post["media_type"],
                post["caption"],  # Add caption
                post["media_id"],
                post["media_url"],
                post["comments"],
                post["tagged_users"],
                post["caption_mentions"],
                post["caption_hashtags"],
                post["location"],
                post["typename"],
                post["owner_username"],
                post["is_sponsored"],
                post["video_duration"],
                post["is_video"],
                post["is_pinned"],
                post["sponsor_users"],
                post["is_paid_partnership"],
                post["boosted_status"],
                post["like_and_view_counts_disabled"],
                post["link"],
                viral,
                viral_score,
                engagement_rate,
                avg_likes,
                avg_comments,
                post["full_metadata"]
            ])
        
        except IndexError as e:
            print(f"Index error occurred while processing post for {username}: {e}. Skipping post.")
            continue  # Skip to the next post if this error occurs
        except Exception as e:
            print(f"An error occurred while processing post for {username}: {e}. Skipping post.")
            continue  # Skip any other unexpected errors

    return bestposts


def export_to_csv(csv_data, filename="instagram_data_regular.csv"):
    """Exports all post data to a CSV file."""
    headers = [
        "Username", "Full Name", "Follower Count", "Following Count", "Total Posts",
        "Likes", "Views", "Timestamp", "Post URL", "Post ID", "Media Type", "Caption",
        "Media ID", "Media URL", "Comments", "Tagged Users", "Caption Mentions", "Caption Hashtags",
        "Location", "Typename", "Owner Username", "Is Sponsored", "Video Duration", "Is Video",
        "Is Pinned", "Sponsor Users", "Is Paid Partnership", "Boosted Status", "Like and View Counts Disabled",
        "Link", "Is Viral?", "Viral Score", "Engagement Rate", "Avg Likes", "Avg Comments", "Full Metadata"
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
#proxy_url = ""  # Replace with your residential proxy details
proxy_url = ""  # Replace with your residential proxy details

configure_proxy(proxy_url)  # Set the proxy configuration for Instaloader

# Create an instance of Instaloader
L = instaloader.Instaloader()

# List of Instagram pages to analyze
pages_to_analyze = "changeurperception womensfutures fearlessfemales.club onlinesuccessqueens selfdeterminedwomen empirebosswoman unstoppable__her thealphawomenclub confidentlywomen myeasytherapy sheempowersall successwomanera empower.femalefreedom femmenology womenlyconfidence bossbabefocus ahustlingbossbabe womanceogossip womenwholeadempires femaleboss_mindset femalempire.co herempoweringmindset femalebusinesspower heramazingmindset iam.affirmations myselflovesupply thirdeyethoughts risingwoman successwomanera femalealphaclub riseinspiredwoman"
pageslist = pages_to_analyze.split(" ")

viralPostData = [["a", 0]] * 9  # Initialize with dummy data
csv_data = []  # List to store all data for CSV export

# Analyze each page for viral content
for user in pageslist:
    viralPostData = find_posts(user, viralPostData, time_imported, csv_data, L)

# Export data to CSV
export_to_csv(csv_data)
print("Instagram data exported to instagram_data.csv.")