from flask import Flask, Response
import os

app = Flask(__name__)

PLAYLIST_DIR = "playlists"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
