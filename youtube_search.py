import os
import json
import requests

API_KEY = os.getenv("YOUTUBE_API_KEY")


def search_videos(keyword):
    if not API_KEY:
        print("YouTube API key missing")
        return []

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "order": "viewCount",
        "maxResults": 50,
        "key": API_KEY
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json().get("items", [])


def main():
    with open("ideas.json", encoding="utf-8") as file:
        ideas = json.load(file)

    for keyword in ideas["search_terms"]:
        print("\nSearching:", keyword)

        videos = search_videos(keyword)

        for video in videos:
            title = video["snippet"]["title"]
            video_id = video["id"]["videoId"]

            print("Title:", title)
            print("Link: https://youtube.com/watch?v=" + video_id)


if __name__ == "__main__":
    main()
