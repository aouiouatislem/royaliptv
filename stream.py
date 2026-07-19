from flask import redirect
import database

def play(stream_id):
    try:
        stream_id = int(stream_id)
    except:
        return "Invalid Stream", 404

    for ch in database.channels:
        if ch["id"] == stream_id:
            return redirect(ch["url"], code=302)

    return "Stream Not Found", 404
