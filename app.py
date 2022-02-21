from prd import *
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('prdsearch.html')


@app.route('/prd_search_init', methods=["GET"])
def prd_search():
    keyword = request.args.get('keyword')
    data = prd(keyword)

    return data

if __name__ == '__main__' :
    app.run('0.0.0.0', port=5000, debug=True)