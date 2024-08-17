try:
    from __main__ import app
except ImportError:
    from main import app
from functools import wraps
import json
import requests
import src.tools.repositories as repositories

from flask import Response, abort, request


# ===================== 创建回应 ===================== #
# 错误处理
@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return json_rsp_common(repositories.RES_FAIL, f"{e.description}")


# 自定义json响应
def json_rsp(code, data):
    return Response(
        json.dumps({"retcode": code} | data, separators=(",", ":")),
        mimetype="application/json",
    )


def json_rsp_with_msg(code, msg, data):
    return Response(
        json.dumps({"retcode": code, "message": msg} | data, separators=(",", ":")),
        mimetype="application/json",
    )


def json_rsp_common(code, msg):
    return Response(
        json.dumps({"retcode": code, "message": msg}), mimetype="application/json"
    )

# 白名单准入
def ip_whitelist(allowed_ips):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.remote_addr not in allowed_ips:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 信息处理
def forward_request(request, url):
    return requests.get(
        url, headers={"miHoYoCloudClientIP": request_ip(request)}
    ).content

def request_ip(request):
    return request.remote_addr

"""
def forward_request_database(request, url, data):
    return requests.post(
        url, headers={"miHoYoCloudClientIP": request_ip(request)}, data=data
    )
"""