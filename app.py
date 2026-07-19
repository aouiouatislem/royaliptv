from flask import Flask, Response, request
from database import load
import xtream
from auth import login
from stream import play
import os

app = Flask(__name__)

PLAYLIST_DIR = "playlists"

load()

@app.route("/")
def home():
    return "Royal IPTV Server Online"


@app.route("/all.m3u")
def all_m3u():
    output = "#EXTM3U\n"
    
    if os.path.exists(PLAYLIST_DIR):
        for filename in sorted(os.listdir(PLAYLIST_DIR)):
            if filename.lower().endswith(".m3u"):
                with open(os.path.join(PLAYLIST_DIR, filename), "r", encoding="utf-8", errors="ignore") as f:
                    output += f.read().replace("#EXTM3U", "") + "\n"

    return Response(output, mimetype="audio/x-mpegurl")


@app.route("/live/<int:stream_id>")
def live(stream_id):
    return play(stream_id)


@app.route("/player_api.php", methods=["GET", "POST"])
@app.route("/panel_api.php", methods=["GET", "POST"])
def player_api():

    username = request.args.get("username", "")
    password = request.args.get("password", "")
    action = request.args.get("action", "")

    # دعم طلبات الـ POST في حال كان التطبيق يرسل البيانات عبر الـ Body
    if not username:
        username = request.form.get("username", "")
    if not password:
        password = request.form.get("password", "")
    if not action:
        action = request.form.get("action", "")

    if not action:
        return login(username, password)

    if action == "get_live_categories":
        return xtream.live_categories()
        
    elif action == "get_live_streams":
        return xtream.live_streams()
        
    elif action == "get_vod_categories":
        return xtream.vod_categories()
        
    elif action == "get_vod_streams":
        return xtream.vod_streams()
        
    elif action == "get_series_categories":
        return xtream.series_categories()
        
    elif action == "get_series":
        return xtream.series()
        
    elif action == "get_series_info":
        return xtream.series_info()
        
    elif action == "get_short_epg":
        return xtream.short_epg()
        
    elif action == "get_simple_data_table":
        return xtream.simple_data_table()
        
    elif action == "get_live_info":
        return xtream.live_info()
        
    elif action == "get_vod_info":
        return xtream.vod_info()

    return login(username, password)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
