from flask import Flask, request
import json

app = Flask(__name__)

# Dictionary to store the DNS records
dns_database = {}

@app.route('/register', methods=['POST'])
def register():
    # Parse the request body
    data = request.json
    name = data

if __name__ == '__main__':
    app.run(port=53533)