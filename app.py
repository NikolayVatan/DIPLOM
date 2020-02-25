from flask import Flask, request, json, jsonify, render_template
from giphypr import search

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.route('/search')
def index():
    tag = request.args.get('tag')
    if not tag:
        return jsonify({'error': 'invalid tag'})
    result = search(tag)
    return render_template('index.html', videos=result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3122)
