import os
import time
import re
import urllib.request

SOURCE_URL = "http://195.201.203.169:8080/get.php?username=admin&password=admin123&type=m3u_plus"

live_categories = {}
vod_categories = {}
series_categories = {}

lives = []
movies = []
series_list = []
series_episodes = {}

def load():
    global lives, movies, series_list, series_episodes
    global live_categories, vod_categories, series_categories

    lives = []
    movies = []
    series_list = []
    series_episodes = {}
    
    live_categories = {}
    vod_categories = {}
    series_categories = {}

    current_timestamp = str(int(time.time()))
    print("Fetching and splitting M3U... Please wait.")
    
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'VLC/3.0.16 LibVLC/3.0.16'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching the link: {e}")
        return

    lines = content.splitlines()
    current_extinf = ""
    
    series_name_to_id = {}
    series_id_counter = 1
    live_id_counter = 1
    movie_id_counter = 1
    episode_id_counter = 1

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("#EXTINF"):
            current_extinf = line
        elif line.startswith("http"):
            if not current_extinf:
                continue
                
            name = current_extinf.split(",", 1)[-1].strip()
            
            # استخراج التصنيف
            match_cat = re.search(r'group-title="([^"]+)"', current_extinf)
            category_name = match_cat.group(1).strip() if match_cat else "Uncategorized"
            
            # استخراج الأيقونة
            match_logo = re.search(r'tvg-logo="([^"]+)"', current_extinf)
            stream_icon = match_logo.group(1).strip() if match_logo else ""

            # الفرز الذكي بناءً على رابط محتوى الميديا
            if "/movie/" in line:
                if category_name not in vod_categories:
                    vod_categories[category_name] = len(vod_categories) + 1
                
                ext_match = re.search(r'\.([a-zA-Z0-9]+)$', line.split("?")[0])
                container = ext_match.group(1) if ext_match else "mp4"

                movies.append({
                    "num": movie_id_counter,
                    "name": name,
                    "stream_type": "movie",
                    "stream_id": movie_id_counter,
                    "stream_icon": stream_icon,
                    "category_id": str(vod_categories[category_name]),
                    "added": current_timestamp,
                    "container_extension": container,
                    "custom_sid": "",
                    "direct_source": line
                })
                movie_id_counter += 1

            elif "/series/" in line:
                if category_name not in series_categories:
                    series_categories[category_name] = len(series_categories) + 1
                
                # استخراج الموسم والحلقة بريجكس ذكي يدعم S01E01 أو 1x01
                season = 1
                episode = 1
                series_name = name
                
                match_se = re.search(r"(.*?)\s+[Ss](\d+)\s*[Ee](\d+)", name, re.IGNORECASE)
                if match_se:
                    series_name = match_se.group(1).strip()
                    season = int(match_se.group(2))
                    episode = int(match_se.group(3))
                else:
                    match_se2 = re.search(r"(.*?)\s+(\d+)x(\d+)", name)
                    if match_se2:
                        series_name = match_se2.group(1).strip()
                        season = int(match_se2.group(2))
                        episode = int(match_se2.group(3))

                if series_name not in series_name_to_id:
                    s_id = series_id_counter
                    series_name_to_id[series_name] = s_id
                    series_list.append({
                        "num": s_id,
                        "name": series_name,
                        "series_id": s_id,
                        "cover": stream_icon,
                        "plot": "",
                        "cast": "",
                        "director": "",
                        "genre": "",
                        "releaseDate": "",
                        "last_modified": current_timestamp,
                        "rating": "0",
                        "category_id": str(series_categories[category_name])
                    })
                    series_id_counter += 1
                
                s_id = series_name_to_id[series_name]
                if s_id not in series_episodes:
                    series_episodes[s_id] = []
                    
                ext_match = re.search(r'\.([a-zA-Z0-9]+)$', line.split("?")[0])
                container = ext_match.group(1) if ext_match else "mp4"

                series_episodes[s_id].append({
                    "id": episode_id_counter,
                    "title": name,
                    "container_extension": container,
                    "info": {},
                    "custom_sid": "",
                    "added": current_timestamp,
                    "season": season,
                    "episode": episode,
                    "direct_source": line
                })
                episode_id_counter += 1

            else:
                if category_name not in live_categories:
                    live_categories[category_name] = len(live_categories) + 1
                
                lives.append({
                    "num": live_id_counter,
                    "name": name,
                    "stream_type": "live",
                    "stream_id": live_id_counter,
                    "stream_icon": stream_icon,
                    "category_id": str(live_categories[category_name]),
                    "epg_channel_id": "",
                    "added": current_timestamp,
                    "custom_sid": "",
                    "tv_archive": 0,
                    "direct_source": line,
                    "tv_archive_duration": 0
                })
                live_id_counter += 1

            current_extinf = ""

    print(f"Loaded {len(live_categories)} Live Cats, {len(lives)} Live Streams.")
    print(f"Loaded {len(vod_categories)} Movie Cats, {len(movies)} Movies.")
    print(f"Loaded {len(series_categories)} Series Cats, {len(series_list)} Series.")
