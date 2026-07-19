from flask import Flask, Response
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Royal IPTV is running"

@app.route("/all.m3u")
def playlist():
    content = "#EXTM3U\n"
    for f in os.listdir("."):
        if f.endswith(".m3u"):
            with open(f, "r", encoding="utf-8", errors="ignore") as file:
                data = file.read()
                data = data.replace("#EXTM3U", "").strip()
                content += "\n" + data
    return Response(content, mimetype="audio/x-mpegurl")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
