from flask import jsonify
from config import *
import time
from datetime import datetime

def login(username, password):
    now_ts = int(time.time())
    now_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if username != USERNAME or password != PASSWORD:
        return jsonify({
            "user_info": {
                "auth": 0,
                "status": "Disabled"
            }
        })

    return jsonify({
        "user_info": {
            "username": USERNAME,
            "password": PASSWORD,
            "message": "Logged In Successfully",
            "auth": 1,
            "status": "Active",
            "exp_date": "1999999999", # Timestamp لتاريخ انتهاء بعيد
            "is_trial": "0",
            "active_cons": "0",
            "created_at": "1600000000",
            "max_connections": str(MAX_CONNECTIONS),
            "allowed_output_formats": [
                "ts",
                "m3u8"
            ]
        },
        "server_info": {
            "url": HOST.replace("https://", "").replace("http://", ""),
            "port": "443",
            "https_port": "443",
            "server_protocol": "https",
            "rtmp_port": "1935",
            "timezone": TIMEZONE,
            "timestamp_now": now_ts,
            "time_now": now_dt,
            "is_cluster": "0"
        }
    })
