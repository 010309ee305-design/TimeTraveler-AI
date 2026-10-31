import json
import yt_dlp


def search_videos(keyword):
    options = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "skip_download": True
    }

    results = []

    with yt_dlp.YoutubeDL(options) as ydl:
        data = ydl.extract_info(
            "ytsearch20:" + keyword,
            download=False
        )

        if not data:
            return results

        for video in data.get("entries", []):
            if not video:
                continue

            results.append({
                "title": video.get("title", "بدون عنوان"),
                "views": video.get("view_count") or 0,
                "link": video.get("webpage_url") or (
                    "https://www.youtube.com/watch?v=" +
                    video.get("id", "")
                )
            })

    return results


def main():
    with open("ideas.json", encoding="utf-8") as file:
        ideas = json.load(file)

    all_videos = {}

    for keyword in ideas["search_terms"]:
        print("جاري البحث:", keyword)

        try:
            videos = search_videos(keyword)

            for video in videos:
                all_videos[video["link"]] = video

        except Exception as error:
            print("حدث خطأ:", error)

    sorted_videos = sorted(
        all_videos.values(),
        key=lambda x: x["views"],
        reverse=True
    )

    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(
            sorted_videos,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("\nتم حفظ النتائج!")

    for video in sorted_videos[:20]:
        print("\nالعنوان:", video["title"])
        print("المشاهدات:", video["views"])
        print("الرابط:", video["link"])


if __name__ == "__main__":
    main()
