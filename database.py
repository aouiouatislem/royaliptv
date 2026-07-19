import os

PLAYLISTS_DIR = os.path.join(os.path.dirname(__file__), "playlists")

channels = []
categories = {}

def load():
    global channels, categories

    channels = []
    categories = {}

    cid = 1

    for file in sorted(os.listdir(PLAYLISTS_DIR)):
        if not file.endswith(".m3u"):
            continue

        category = os.path.splitext(file)[0]

        if category not in categories:
            categories[category] = len(categories) + 1

        path = os.path.join(PLAYLISTS_DIR, file)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF") and i + 1 < len(lines):
                name = lines[i].split(",", 1)[-1].strip()
                url = lines[i + 1].strip()

                channels.append({
                    "id": cid,
                    "name": name,
                    "url": url,
                    "category_id": categories[category],
                    "category_name": category
                })

                cid += 1

    print("Categories:", len(categories))
    print("Channels:", len(channels))
