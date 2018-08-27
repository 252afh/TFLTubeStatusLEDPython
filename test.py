import requests
from Settings import ApiUrl
from flask import Flask, jsonify, current_app

def getLinesByMode(mode):
    with current_app.app_context():
        if mode is None:
            return Response("The supplied mode is empty", 422)
        result = requests.get('{}Line/Mode/{}'.format(ApiUrl, mode))
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def test(mode):
    result = requests.get('{}Line/Mode/{}'.format(ApiUrl, mode))
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)