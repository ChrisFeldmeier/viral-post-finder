import time
import instaloader

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
    """Fetches Instagram posts using Instaloader."""
    L = instaloader.Instaloader()

    try:
        # Load the profile
        profile = instaloader.Profile.from_username(L.context, username)
        
        posts_data = []
        
        # Iterate over profile's posts
        for post in profile.get_posts():
            posts_data.append({
                "likes": post.likes,
                "views": post.video_view_count if post.is_video else None,  # Add view count for videos
                "timestamp": post.date_utc,
                "url": post.url,
                "shortcode": post.shortcode,  # Use shortcode for the post ID
                "media_type": "video" if post.is_video else "photo"  # Treat Reels as videos
            })
            
            # Optionally, limit the number of posts fetched
            if len(posts_data) >= 12:
                break
        
        return posts_data
    except Exception as e:
        print(f"Error fetching data for {username}: {e}")
        return None

def find_posts(username, bestposts, time_imported):
    """Find viral posts based on views for videos and likes for photos, and time frame."""
    posts_info = fetch_instagram_data(username)
    
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
    for post in range(len(likesOnPosts)):
        if likesOnPosts[post] > averageLikes + (0.6 * averageLikes):  # If it's considered a viral post
            viral_score = 1 - (averageLikes / likesOnPosts[post])  # Viral score
            print(f"{username} : Viral Post Found: https://www.instagram.com/p/{idsOnPosts[post]} - Viral Score: {viral_score * 100:.2f}%")
            if viral_score > bestposts[0][1]:  # If score higher than on current list, replace it
                bestposts.pop(0)
                bestposts.append([idsOnPosts[post], viral_score])
                bestposts.sort(key=lambda x: x[1])

    return bestposts

# Initialize user input
mediaType = ""
time_imported = ""

def run_intro():
    mediaType = ""
    time_imported = input("Within how many days should the post be? ")
    if mediaType not in ["v", "b", "p"]:
        print("Error, only type v, b, or p")
    if not time_imported.isdigit():
        print("Error, use only positive numbers for the days.")
    return time_imported, mediaType

# Main execution flow
while mediaType not in ["v", "b", "p"] or not time_imported.isdigit():
    time_imported, mediaType = run_intro()

pages_to_analyze = input("Type usernames separated by a space to analyze for viral content: ")
pageslist = pages_to_analyze.split(" ")
viralPostData = [["a", 0], ["b", 0], ["c", 0], ["d", 0], ["e", 0], ["f", 0], ["g", 0], ["h", 0], ["i", 0]]  # Empty list to start with

# Analyze each page for viral content
for user in pageslist:
    viralPostData = find_posts(user, viralPostData, time_imported)

# Display viral posts
for item in viralPostData:
    if item[1] != 0:
        print("\n" + "Post: https://www.instagram.com/p/" + item[0] + " Score: " + str(item[1] * 100))
