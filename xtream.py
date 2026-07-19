from flask import jsonify
import database

def live_categories():
    return jsonify([
        {
            "category_id": str(cid),
            "category_name": name,
            "parent_id": 0
        }
        for name, cid in database.categories.items()
    ])


def live_streams():
    data = []

    for ch in database.channels:
        data.append({
            "num": ch["id"],
            "name": ch["name"],
            "stream_type": "live",
            "stream_id": ch["id"],
            "stream_icon": "",
            "epg_channel_id": "",
            "added": ch.get("added", "1600000000"),
            "category_id": str(ch["category_id"]),
            "custom_sid": "",
            "tv_archive": 0,
            "direct_source": ch["url"],
            "tv_archive_duration": 0
        })

    return jsonify(data)

# دوال لتجنب Crash عند محاولة التطبيق جلب VOD و Series
def vod_categories():
    return jsonify([])

def vod_streams():
    return jsonify([])

def series_categories():
    return jsonify([])

def series():
    return jsonify([])

def series_info():
    return jsonify({})

def short_epg():
    return jsonify({"epg_listings": []})

def live_info():
    return jsonify({"info": {}})

def vod_info():
    return jsonify({"info": {}})

def simple_data_table():
    # بعض التطبيقات تطلب هذا الـ action لجلب كل شيء دفعة واحدة
    return jsonify({
        "categories": [
            {
                "category_id": str(cid),
                "category_name": name,
                "parent_id": 0
            }
            for name, cid in database.categories.items()
        ],
        "streams": []
    })
