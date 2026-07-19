from flask import Flask, Response, request
from database import load
import xtream
from auth import login
from stream import play
import os

app = Flask(__name__)

load()

@app.route("/")
def home():
    return "Royal IPTV Server Online"

# مسارات توجيه البث القياسية لـ Xtream Codes لتجنب الـ 404
@app.route("/live/<username>/<password>/<stream_id_ext>")
def live_stream(username, password, stream_id_ext):
    stream_id = stream_id_ext.split(".")[0]
    return play(stream_id, "live")

@app.route("/movie/<username>/<password>/<stream_id_ext>")
def movie_stream(username, password, stream_id_ext):
    stream_id = stream_id_ext.split(".")[0]
    return play(stream_id, "movie")

@app.route("/series/<username>/<password>/<stream_id_ext>")
def series_stream(username, password, stream_id_ext):
    stream_id = stream_id_ext.split(".")[0]
    return play(stream_id, "series")


@app.route("/player_api.php", methods=["GET", "POST"])
@app.route("/panel_api.php", methods=["GET", "POST"])
def player_api():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    action = request.args.get("action", "")

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
