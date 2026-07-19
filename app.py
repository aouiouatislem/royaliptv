from flask import Flask, Response, request
from database import load
from xtream import live_categories, live_streams
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

    for filename in sorted(os.listdir(PLAYLIST_DIR)):
        if filename.lower().endswith(".m3u"):
            with open(os.path.join(PLAYLIST_DIR, filename), "r", encoding="utf-8", errors="ignore") as f:
                output += f.read().replace("#EXTM3U", "") + "\n"

    return Response(output, mimetype="audio/x-mpegurl")


@app.route("/live/<int:stream_id>")
def live(stream_id):
    return play(stream_id)


@app.route("/player_api.php")
def player_api():

    username = request.args.get("username", "")
    password = request.args.get("password", "")
    action = request.args.get("action", "")

    if action == "":
        return login(username, password)

    if action == "get_live_categories":
        return live_categories()

    if action == "get_live_streams":
        return live_streams()

    return login(username, password)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
