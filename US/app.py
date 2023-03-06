from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # Get the parameters from the query string
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Check if all required parameters are present
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad request", 400

    # Query the Authoritative Server for the IP address of the given hostname
    dns_query = {'Name': hostname, 'Type': 'A'}
    response = requests.get(f'http://{as_ip}:{as_port}/dns', params=dns_query)

    if response.status_code != 200:
        return "DNS query failed", 500

    ip_address = response.json()['Value']

    # Query the Fibonacci Server for the Fibonacci number
    fs_query = {'number': number}
    response = requests.get(f'http://{ip_address}:{fs_port}/fibonacci', params=fs_query)

    if response.status_code != 200:
        return "Fibonacci query failed", 500

    return response.text, 200

if __name__ == '__main__':
    app.run(port=8080)
