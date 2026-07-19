from flask import jsonify
from database import channels, categories

def live_categories():
    return jsonify([
        {
            "category_id": str(cid),
            "category_name": name,
            "parent_id": 0
        }
        for name, cid in categories.items()
    ])


def live_streams():
    data = []

    for ch in channels:
        data.append({
            "num": ch["id"],
            "name": ch["name"],
            "stream_type": "live",
            "stream_id": ch["id"],
            "stream_icon": "",
            "category_id": str(ch["category_id"]),
            "epg_channel_id": "",
            "added": "0",
            "custom_sid": "",
            "tv_archive": 0,
            "direct_source": ch["url"]
        })

    return jsonify(data)
