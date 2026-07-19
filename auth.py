from flask import jsonify

USERNAME = "royal"
PASSWORD = "123"

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
            "max_connections": 1,
            "active_cons": 0
        },
        "server_info": {
            "url": "royaliptv.onrender.com",
            "https_port": "443",
            "server_protocol": "https",
            "timezone": "UTC"
        }
    })
