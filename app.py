from flask import Flask, Response
import os
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Royal IPTV"

@app.route("/all.m3u")
def playlist():
    output = "#EXTM3U\n"

    for filename in sorted(os.listdir(".")):
        if filename.lower().endswith(".m3u"):
            category = os.path.splitext(filename)[0]

            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for line in lines:
                if line.startswith("#EXTINF"):
                    if "group-title=" in line:
                        line = re.sub(r'group-title="[^"]*"', f'group-title="{category}"', line)
                    else:
                        line = line.replace(",", f' group-title="{category}",')
                output += line

    return Response(output, mimetype="audio/x-mpegurl")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
