from flask import jsonify, request
import database

def live_categories():
    return jsonify([
        {"category_id": str(cid), "category_name": name, "parent_id": 0}
        for name, cid in database.live_categories.items()
    ])

def live_streams():
    category_id = request.args.get("category_id")
    if category_id:
        return jsonify([ch for ch in database.lives if ch["category_id"] == str(category_id)])
    return jsonify(database.lives)

def vod_categories():
    return jsonify([
        {"category_id": str(cid), "category_name": name, "parent_id": 0}
        for name, cid in database.vod_categories.items()
    ])

def vod_streams():
    category_id = request.args.get("category_id")
    if category_id:
        return jsonify([m for m in database.movies if m["category_id"] == str(category_id)])
    return jsonify(database.movies)

def series_categories():
    return jsonify([
        {"category_id": str(cid), "category_name": name, "parent_id": 0}
        for name, cid in database.series_categories.items()
    ])

def series():
    category_id = request.args.get("category_id")
    if category_id:
        return jsonify([s for s in database.series_list if s["category_id"] == str(category_id)])
    return jsonify(database.series_list)

def series_info():
    try:
        sid = int(request.args.get("series_id", 0))
    except:
        return jsonify({})
        
    episodes = database.series_episodes.get(sid, [])
    
    seasons_dict = {}
    for ep in episodes:
        s_num = str(ep["season"])
        if s_num not in seasons_dict:
            seasons_dict[s_num] = []
        seasons_dict[s_num].append(ep)
        
    info = {}
    for s in database.series_list:
        if s["series_id"] == sid:
            info = {
                "name": s["name"],
                "cover": s["cover"],
                "plot": s["plot"],
                "cast": s["cast"],
                "director": s["director"],
                "genre": s["genre"],
                "releaseDate": s["releaseDate"],
                "rating": s["rating"]
            }
            break

    return jsonify({
        "seasons": [
            {"air_date": "", "episode_count": len(v), "id": int(k), "name": f"Season {k}", "overview": "", "season_number": int(k)}
            for k, v in seasons_dict.items()
        ],
        "info": info,
        "episodes": seasons_dict
    })

def short_epg():
    return jsonify({"epg_listings": []})

def live_info():
    return jsonify({"info": {}})

def vod_info():
    return jsonify({"info": {}})

def simple_data_table():
    return jsonify({
        "categories": [
            {"category_id": str(cid), "category_name": name, "parent_id": 0}
            for name, cid in database.live_categories.items()
        ],
        "streams": []
    })
