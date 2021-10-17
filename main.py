import json
import subprocess
import sys
import uuid
from flask import Flask, request

app = Flask(__name__)

with open("./config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

@app.route("/")
def index():
    return "<p></p>"

@app.route("/v2/check/<license>", methods=["GET", "POST"])
def check(license):
    with open("./licenses/d.json", "r", encoding="utf-8") as f:
        licenses = json.load(f)

    if license not in licenses:
        return {
            "error": "license not found"
        }, 404
    elif license in licenses:
        blacklisted = licenses[license]

        return {
            "license": f"{license}",
            "blacklisted": blacklisted
        }, 200

@app.route("/v2/create/", methods=["GET", "POST"])
def create():
    with open("./licenses/d.json", "r", encoding="utf-8") as f:
        licenses = json.load(f)

    license_key = str(uuid.uuid4().hex)
    license_key = license_key[:15]
    licenses[f"{license_key}"] = False

    with open("./licenses/d.json", 'w') as f:
        json.dump(licenses, f, indent=2)

    return {
        "license": f"{license_key}",
    }, 200

@app.route("/v2/delete/<license>", methods=["GET", "POST"])
def delete(license):
    with open("./licenses/d.json", "r", encoding="utf-8") as f:
        licenses = json.load(f)

    if license not in licenses:

        return {
            "error": "license not found"
        }, 404

    elif license in licenses:
        del licenses[license]

        with open("./licenses/d.json", 'w') as f:
            json.dump(licenses, f, indent=2)

        return {
            "success": True
        }, 200

@app.route("/v2/blacklist/<license>", methods=["GET", "POST"])
def blacklist(license):
    with open("./licenses/d.json", "r", encoding="utf-8") as f:
        licenses = json.load(f)

    if license not in licenses:

        return {
            "error": "license not found"
        }, 404

    elif license in licenses:
        if licenses[license] is True:
            return {
                "error": "license already blacklisted"
            }, 400

        licenses[license] = True

        with open("./licenses/d.json", 'w') as f:
            json.dump(licenses, f, indent=2)

        return {
            "success": True
        }, 200

@app.route("/v2/unblacklist/<license>", methods=["GET", "POST"])
def unblacklist(license):
    with open("./licenses/d.json", "r", encoding="utf-8") as f:
        licenses = json.load(f)

    if license not in licenses:

        return {
            "error": "license not found"
        }, 404

    elif license in licenses:
        if licenses[license] is False:
            return {
                "error": "license not blacklisted"
            }, 400

        licenses[license] = False

        with open("./licenses/d.json", 'w') as f:
            json.dump(licenses, f, indent=2)

        return {
            "success": True
        }, 200


if __name__ == "__main__":
    app.run(port=config['server_port'], debug=True)
