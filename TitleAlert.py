import asyncio
from datetime import datetime
import asyncpraw
import sys

# Config API Reddit
# https://developers.reddit.com/docs/api
# https://business.reddithelp.com/s/article/Create-a-Reddit-Application

async def create_reddit_client():
    reddit = asyncpraw.Reddit(
        client_id="provided by reddit api",
        client_secret="provided by reddit api",
        user_agent="TitleAlert/0.1 by 74:n",
    )
    return reddit

# Subreddits
subreddits = ["artcommissions", "Artistsforhire", "comissions"] # Examples of Subs I've used to get commissions for drawings

# List of keywords to search for
keywords = ["Hiring", "Looking for an artist", "Looking for artist"] # Examples

# List to store IDs of posts already seen
seen_posts = set()

async def check_new_posts(reddit):
    """Checks for new posts in the specified subreddits and reports the link to those that contain keywords."""
    for subreddit_name in subreddits:
        for i in range(10):  # Loop to create the loading effect
            sys.stdout.flush()
            await asyncio.sleep(0.1)  # Wait a short while for the loading to update
        
        subreddit = await reddit.subreddit(subreddit_name)

        async for submission in subreddit.new(limit=10):  # Check the 10 most recent posts
            if submission.id not in seen_posts:
                seen_posts.add(submission.id)  # Mark the post as seen

                # Check if the title contains any of the keywords
                if any(keyword.lower() in submission.title.lower() for keyword in keywords):
                    post_time = datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    subreddit_link = f"https://www.reddit.com/r/{subreddit_name}"
                    user_link = f"https://www.reddit.com/user/{submission.author}"
                    
                    print("\n-----------------------------------------------------------")
                    print(f"Subreddit: {subreddit_name} ({subreddit_link})")
                    print(f"Date and time: {post_time}")
                    print(f"Title: {submission.title}")
                    print(f"Post: {submission.url}")
                    print(f"User: {submission.author} ({user_link})")
                    print("-----------------------------------------------------------")

async def main():
    print("Starting monitoring...")

    reddit = await create_reddit_client()

    try:
        while True:
            await check_new_posts(reddit)
            await asyncio.sleep(120)  # Wait 120 seconds before checking again
    except KeyboardInterrupt:
        print("\nMonitoring closed.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop() 
    if loop.is_running():
        print("The event loop is already running, waiting.")
        loop.create_task(main()) 
    else:
        loop.run_until_complete(main())  # If the loop is not running, run it normally
