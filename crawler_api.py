from hikerapi import Client, AsyncClient
import csv
from datetime import datetime

def calculate_engagement_rate(posts_data, follower_count):
    """Calculates the engagement rate based on the last 16 images."""
    total_likes = sum(post['like_count'] for post in posts_data)
    total_comments = sum(post.get('comment_count', 0) for post in posts_data)
    engagement_rate = (total_likes + total_comments) / (follower_count * len(posts_data)) * 100
    avg_likes = total_likes / len(posts_data)
    avg_comments = total_comments / len(posts_data) if total_comments else 0
    return engagement_rate, avg_likes, avg_comments

def export_to_csv(all_medias, filename="instagram_data.csv"):
    """Exports media data to a CSV file for multiple users."""
    headers = [
        "Username", "Full Name", "Follower Count", "Following Count", "Total Posts",
        "Likes", "Views", "Timestamp", "Post URL", "Post ID", "Media Type", "Caption",
        "Media ID", "Media URL", "Comments", "Tagged Users", "Caption Mentions", "Caption Hashtags",
        "Location", "Typename", "Owner Username", "Is Sponsored", "Video Duration", "Is Video",
        "Is Pinned", "Sponsor Users", "Is Paid Partnership", "Boosted Status", "Like and View Counts Disabled",
        "Link", "Is Viral?", "Viral Score", "Engagement Rate", "Avg Likes", "Avg Comments"
    ]

    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        
        for user_medias in all_medias:

            items = user_medias['response']['items']
            profile_data = user_medias['response']['user']
            username = user_medias['response']['user'].get('username', "")
            follower_count = profile_data.get('follower_count', 1)  # Default to 1 to avoid division by zero
            #user_id = user_medias['response']['user'].get('id', "")
            #user_data = cl.user_info_v2(user_id=user_id) #API Call
            #user_id = user_data.graphql.user.edge_followed_by.count
            #follower_count = user_data.graphql.user.edge_followed_by.count

            # Calculate engagement rate, avg likes, avg comments
            engagement_rate, avg_likes, avg_comments = calculate_engagement_rate(items, follower_count)

            for item in items:
                # Convert 'taken_at' to datetime
                taken_at = datetime.fromtimestamp(item.get('taken_at', 0))

                # Determine if the post is viral
                likes = item.get('like_count', 0)
                viral = likes > avg_likes + (0.6 * avg_likes)
                viral_score = (likes / avg_likes) - 1 if viral else 0

                row = {
                    "Username": item.get('user', {}).get('username', ''),
                    "Full Name": item.get('user', {}).get('full_name', ''),
                    "Follower Count": follower_count,
                    "Following Count": '',  # Not available in this response
                    "Total Posts": '',  # Not available in this response
                    "Likes": likes,
                    "Views": item.get('play_count', 0),
                    "Timestamp": taken_at.isoformat(),
                    "Post URL": f"https://www.instagram.com/p/{item.get('code', '')}/",
                    "Post ID": item.get('pk', ''),
                    "Media Type": item.get('media_type', ''),
                    "Caption": item.get('caption', {}).get('text', ''),
                    "Media ID": item.get('id', ''),
                    "Media URL": item.get('image_versions2', {}).get('candidates', [{}])[0].get('url', ''),
                    "Comments": item.get('comment_count', 0),
                    "Tagged Users": ', '.join([user.get('username', '') for user in item.get('usertags', [])]),
                    "Caption Mentions": '',  # Not directly available in this response
                    "Caption Hashtags": '',  # Not directly available in this response
                    "Location": '',  # Not available in this response
                    "Typename":  item.get('media_type', ''),  # Not available in this response
                    "Owner Username": item.get('user', {}).get('username', ''),
                    "Is Sponsored": item.get('is_paid_partnership', False),
                    "Video Duration": item.get('video_duration', 0),
                    "Is Video": item.get('media_type', 0) == 2,
                    "Is Pinned": '',  # Not available in this response
                    "Sponsor Users": '',  # Not available in this response
                    "Is Paid Partnership": item.get('is_paid_partnership', False),
                    "Boosted Status": '',  # Not available in this response
                    "Like and View Counts Disabled": item.get('like_and_view_counts_disabled', False),
                    "Link": '',  # Not available in this response
                    "Is Viral?": viral,
                    "Viral Score": viral_score,
                    "Engagement Rate": engagement_rate,
                    "Avg Likes": avg_likes,
                    "Avg Comments": avg_comments,
                }
                writer.writerow(row)

# Your existing code
cl = Client("NmLAGEj8ThCiP0oJRrGi68xRmNFtCvzv")
#cl._url = "http://localhost:3000"

# List of user IDs to process (Instagram User IDs)
user_ids = ["8397181423"]  # Add more user IDs as needed

all_medias = []
for user_id in user_ids:
    medias = cl.user_medias_v2(user_id=user_id, page_id=None)
    all_medias.append(medias)

# Export the data to CSV
export_to_csv(all_medias)

print("Data exported to instagram_data.csv")