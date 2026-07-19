import os
import time
import re
import urllib.request

# الرابط الخاص بك
SOURCE_URL = "http://195.201.203.169:8080/get.php?username=admin&password=admin123&type=m3u_plus"

channels = []
categories = {}

def load():
    global channels, categories

    channels = []
    categories = {}

    cid = 1
    current_timestamp = str(int(time.time()))

    print("Fetching M3U from source link... Please wait.")
    
    # نستخدم User-Agent لتفادي الحظر من السيرفر الأصلي
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'VLC/3.0.16 LibVLC/3.0.16'})
    
    try:
        with urllib.request.urlopen(req) as response:
            # قراءة الملف وفك تشفيره
            content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching the link: {e}")
        return

    lines = content.splitlines()
    
    current_name = ""
    current_category = "Uncategorized"

    print("Parsing channels and categories in memory...")

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # إذا كان السطر يحتوي على معلومات القناة
        if line.startswith("#EXTINF"):
            # استخراج اسم القناة (الكلمات بعد آخر فاصلة)
            current_name = line.split(",", 1)[-1].strip()
            
            # استخراج اسم التصنيف من group-title
            match = re.search(r'group-title="([^"]+)"', line)
            if match:
                current_category = match.group(1).strip()
            else:
                current_category = "Uncategorized"
                
            # إذا لم يكن التصنيف موجوداً، أضفه وأعطه ID جديد
            if current_category not in categories:
                categories[current_category] = len(categories) + 1
                
        # إذا كان السطر هو الرابط
        elif line.startswith("http"):
            if current_name: # التأكد من وجود اسم للقناة
                channels.append({
                    "id": cid,
                    "name": current_name,
                    "url": line,
                    "category_id": categories[current_category],
                    "category_name": current_category,
                    "added": current_timestamp
                })
                cid += 1
                
            # تصفير المتغيرات استعداداً للقناة القادمة
            current_name = ""
            current_category = "Uncategorized"

    print("Categories Loaded:", len(categories))
    print("Channels/VOD Loaded:", len(channels))
