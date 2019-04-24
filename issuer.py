"""
https://stackoverflow.com/questions/29650495/how-to-verify-a-jwt-using-python-pyjwt-with-public-key
"""

import time

import jwt

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from flask import Flask, request, jsonify


# Load the key we created
with open("/data/private_key", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

app = Flask(__name__)


@app.route("/jwt/auth")
def auth():
    _, p, action = request.args.get('scope').split(':')
    project = p.replace('%2F', '/')
    now = int(time.mktime(time.localtime()))

    claims = dict(aud=request.args.get('service'),
                  sub=request.args.get('client_id'),
                  access=list(
                      dict(type="repository",
                           name=project,
                           actions=list(action)
                           )
                  ),
                  iss="gitlab-issuer",
                  iat=now,
                  nbf=now,
                  exp=now+300,
                  )
    jwt_token = jwt.encode(claims, key=private_key, algorithm='RS256')
    app.logger.info(repr(jwt_token))
    try:
        app.logger.info(jwt.decode(jwt_token, verify=False))
    except Exception:
        app.logger.exception('cant decode token')
    return jsonify(dict(token=jwt_token.decode('utf8')))


if __name__ == "__main__":
    import os
    app.run(debug=(os.getenv("DEBUG") != ""), host="0.0.0.0", port=5000)
