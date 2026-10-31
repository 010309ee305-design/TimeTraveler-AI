
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

RSS_URL = "https://trends.google.com/trending/rss?geo=US"

def get_trends():
    request = urllib.request.Request(
        RSS_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()

    root = ET.fromstring(content)
    results = []

    for item in root.findall(".//item"):
        title = item.findtext("title", "بدون عنوان")
        link = item.findtext("link", "")

        results.append({
            "topic": title,
            "link": link,
            "source": "Google Trends"
        })

    return results

def main():
    print("TimeTraveler AI")
    print("جاري اكتشاف المواضيع الرائجة...")

    try:
        trends = get_trends()

        data = {
            "updated": datetime.now().isoformat(),
            "count": len(trends),
            "trends": trends
        }

        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("تم حفظ النتائج بنجاح!")
        for number, item in enumerate(trends, 1):
            print(f"{number}. {item['topic']}")
            print(item["link"])

    except Exception as error:
        print("تعذر جلب الترندات:", error)
        raise

if __name__ == "__main__":
    main()
