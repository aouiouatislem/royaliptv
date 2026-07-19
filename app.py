from flask import Flask, Response, jsonify, request
from database import load
from xtream import live_categories, live_streams
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

    if not os.path.exists(PLAYLIST_DIR):
        return Response(output, mimetype="audio/x-mpegurl")

    for filename in sorted(os.listdir(PLAYLIST_DIR)):
        if filename.lower().endswith(".m3u"):
            path = os.path.join(PLAYLIST_DIR, filename)

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()

            data = data.replace("#EXTM3U", "").strip()
            output += "\n" + data + "\n"

    return Response(output, mimetype="audio/x-mpegurl")


@app.route("/player_api.php")
def player_api():
    action = request.args.get("action")

    if action == "get_live_categories":
        return live_categories()

    if action == "get_live_streams":
        return live_streams()

    return jsonify({
        "user_info": {
            "username": "royal",
            "password": "123",
            "auth": 1,
            "status": "Active"
        },
        "server_info": {
            "url": "royaliptv.onrender.com",
            "https_port": "443"
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
