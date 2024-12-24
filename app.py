from flask import Flask, request, jsonify
from validator import Validator
from error_handler import register_error_handler
from scrapper import WebScrapper

app = Flask(__name__)
validator = Validator()
web_scrapper = WebScrapper()

# Register error handlers
register_error_handler(app)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/url', methods=['POST'])
def post_message():
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    
    if 'url' not in data:
        return jsonify({'error': 'URL field is required'}), 400
    
    url = data['url']
    validator.url_validator(url=url)
    content = web_scrapper.scrape_url(url)
    
    return jsonify({
        'status': 'success',
        'data': content
    }), 201


if __name__ == '__main__':
    app.run(debug=True)
