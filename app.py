from flask import Flask, request
from requests import request as curl_request
from urllib.parse import quote, urlencode, quote_plus
from config import *

app = Flask(__name__)


def post_to_mattermost(text, channel=CHANNEL, username=USER_NAME, icon=USER_ICON):
    payload = 'payload={"channel":"'+channel+'","text":"'+quote_plus(text)+'","username":"'+username+'"}'
    if DEBUG:
        print(payload)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    response = curl_request("POST", MM_URL+"hooks/"+HOOK_ID, data=payload, headers=headers)
    result = response.text
    if DEBUG:
        print("---hook response---")
        print(result)
    return result


@app.route('/', methods=['GET'])
def hello_world():
    return "Welcome to W3IM"


@app.route('/hooks/<token>', methods=['POST', 'GET'])
def mattermost_jira(token):
    if token == HOOK_ID:
        try:
            data = request.json
        except Exception as ex:
            return str(ex)
        if DEBUG:
            print(data)
            print("-------------")
        if data and data.get("project_name", None) and data.get("message", None):
            if DEBUG:
                print(data['message'])
            sentry_url = "[Click Here For Details]("+data.get("url", "#")+")"

            return post_to_mattermost(text="`"+data['message'].replace('"', '')+"`\n\n" +
                                           sentry_url.replace("/sentry/sentry/", "/sentry/", 1),
                                      username=data['project_name'].replace("-", " ").title())
        else:
            print("Error: Project name and Message Missing!")
            if DEBUG:
                print(data)
    else:
        print("Error: Wrong hook.")

    return token


@app.route('/oauth', methods=['POST', 'GET'])
def oauth():
    return "Thanks for using my app"


if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)
