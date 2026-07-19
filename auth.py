from flask import jsonify
from config import *

def login(username, password):

    if username != USERNAME or password != PASSWORD:
        return jsonify({
            "user_info": {
                "auth": 0,
                "status": "Disabled"
            }
        })

    return jsonify({
        "user_info": {
            "auth": 1,
            "status": "Active",
            "username": USERNAME,
            "password": PASSWORD,
            "max_connections": MAX_CONNECTIONS,
            "active_cons": 0,
            "allowed_output_formats": [
                "ts",
                "m3u8"
            ]
        },
        "server_info": {
            "url": HOST.replace("https://", ""),
            "server_protocol": "https",
            "https_port": "443",
            "timezone": TIMEZONE
        }
    })
