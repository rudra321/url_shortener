from flask import Flask, request, jsonify, render_template
import hashlib
import base64

app = Flask(__name__)

url_mapping = {}
counter = 1

def shorten_url(long_url):
    global counter
    short_id = counter
    counter += 1
    url_hash = hashlib.md5(long_url.encode()).hexdigest()
    short_url = base64.b64encode(url_hash.encode()).decode()[:8]
    url_mapping[short_url] = long_url
    return short_url

def expand_url(short_url):
    return url_mapping.get(short_url, "URL not found")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('long_url')
    if not long_url:
        return jsonify({'error': 'Invalid input'})
    short_url = shorten_url(long_url)
    return jsonify({'short_url': short_url})

@app.route('/search')
def search():
    term = request.args.get('term')
    results = []
    for short_url, long_url in url_mapping.items():
        if term.lower() in long_url.lower():
            results.append({'short': short_url, 'long': long_url})
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)