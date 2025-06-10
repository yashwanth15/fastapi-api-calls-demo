import httpx
from fastapi import HTTPException
import asyncio
import logging
from collections import defaultdict
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_github_user(username: str) -> Dict[str, Any]:
    """
    Fetch basic public details of a GitHub user by username.
    Raises HTTPException if user is not found.
    """
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/users/{username}"
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")

        data = response.json()
        logger.info(f"GitHub user data fetched for {username}")
        return {
            "login": data["login"],
            "name": data.get("name"),
            "public_repos": data["public_repos"],
            "followers": data["followers"]
        }

async def fetch_and_filter_posts() -> List[Dict[str, Any]]:
    """
    Fetch posts and users from JSONPlaceholder and return a list of users
    sorted by their post count.
    """
    async with httpx.AsyncClient() as client:
        posts_res = await client.get("https://jsonplaceholder.typicode.com/posts")
        users_res = await client.get("https://jsonplaceholder.typicode.com/users")

        posts = posts_res.json()
        users = users_res.json()

        user_post_counts = defaultdict(int)
        for post in posts:
            user_post_counts[post["userId"]] += 1

        res = []
        for user in users:
            res.append({
                "user_id": user["id"],
                "user_name": user["username"],
                "email": user["email"],
                "post_count": user_post_counts[user["id"]]
            })

        res.sort(key=lambda x: x["post_count"], reverse=True)
        logger.info("User post counts sorted.")
        return res

async def fetch_and_filter_albums() -> List[Dict[str, Any]]:
    """
    Fetch albums and photos from JSONPlaceholder and return a list of albums
    with photo counts and the first photo as the cover photo.
    """
    async with httpx.AsyncClient() as client:
        albums_res = await client.get("https://jsonplaceholder.typicode.com/albums")
        photos_res = await client.get("https://jsonplaceholder.typicode.com/photos")

        albums = albums_res.json()
        photos = photos_res.json()
        photos.sort(key=lambda x: x['id'])

        album_count = defaultdict(int)
        cover_photo = defaultdict(dict)
        for p in photos:
            album_count[p["albumId"]] += 1
            if not cover_photo[p["albumId"]]:
                cover_photo[p["albumId"]] = p

        res = []
        for album in albums:
            res.append({
                "album_id": album["id"],
                "album_title": album["title"],
                "photo_count": album_count[album["id"]],
                "cover_photo": cover_photo[album["id"]]
            })

        logger.info("Album data compiled with photo counts and covers.")
        return res

async def main() -> None:
    # Example usage: Uncomment one at a time for testing

    # result = await get_github_user("yashwanth15")
    # print(result)

    # posts = await fetch_and_filter_posts()
    # for user in posts:
    #     print(user)

    albums = await fetch_and_filter_albums()
    for album in albums:
        print(album)

if __name__ == "__main__":
    asyncio.run(main())
