from flask import Flask, request
import json

app = Flask(__name__)

# Dictionary to store the hostname-IP mapping
dns_cache = {}

@app.route('/register', methods=['PUT'])
def register():
    # Parse the request body
    data = request.json
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    # Check if all required fields are present
    if not all([hostname, ip, as_ip, as_port]):
        return "Bad request", 400

    # Register the hostname-IP mapping with the Authoritative Server
    dns_registration = {'Name': hostname, 'Value': ip, 'Type': 'A', 'TTL': 10}
    response = requests.post(f'http://{as_ip}:{as_port}/register', json=dns_registration)

    if response.status_code != 201:
        return "DNS registration failed", 500

    # Store the hostname-IP mapping in the cache
    dns_cache[hostname] = ip

    return "Registration successful", 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # Get the parameter from the query string
    number = request.args.get('number')

    # Check if the parameter is present and valid
    if not number or not number.isdigit():
        return "Bad request", 400

    # Calculate the Fibonacci number
    n = int(number)
    fib = fibonacci_helper(n)

    return str(fib), 200

def fibonacci_helper(n):
    if n < 2:
        return n
    else:
        return fibonacci_helper(n-1) + fibonacci_helper(n-2)

if __name__ == '__main__':
    app.run(port=9090)
