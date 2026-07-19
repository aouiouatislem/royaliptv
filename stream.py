from flask import redirect
import database

def play(stream_id, stream_type):
    try:
        stream_id = int(stream_id)
    except:
        return "Invalid Stream ID", 404

    if stream_type == "live":
        for ch in database.lives:
            if ch["stream_id"] == stream_id:
                return redirect(ch["direct_source"], code=302)
                
    elif stream_type == "movie":
        for m in database.movies:
            if m["stream_id"] == stream_id:
                return redirect(m["direct_source"], code=302)
                
    elif stream_type == "series":
        for ep_list in database.series_episodes.values():
            for ep in ep_list:
                if ep["id"] == stream_id:
                    return redirect(ep["direct_source"], code=302)

    return "Stream Not Found", 404
