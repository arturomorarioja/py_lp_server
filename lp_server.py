import argparse
import queue
import time
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

messages = queue.Queue()


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/send', methods=['POST', 'OPTIONS'])
def send_message():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400

    print('Received from client:', data)
    messages.put(data)

    return jsonify({
        'status': 'accepted'
    }), 202


@app.get('/poll')
def poll():
    timeout_seconds = 20
    start_time = time.time()

    while True:
        try:
            data = messages.get_nowait()
            return jsonify({
                'type': 'echo',
                'received': data
            }), 200
        except queue.Empty:
            if time.time() - start_time >= timeout_seconds:
                return jsonify({
                    'type': 'timeout',
                    'message': 'No new messages'
                }), 200

            time.sleep(0.2)


@app.get('/hello')
def hello():
    return jsonify({
        'message': 'Hello from server!'
    }), 200


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Simple long-polling server.'
    )
    parser.add_argument(
        'port',
        nargs='?',
        type=int,
        default=8080,
        help='Port to listen on (default: 8080)'
    )

    args = parser.parse_args()

    print(f'Long-polling server running on http://localhost:{args.port}')
    app.run(host='localhost', port=args.port, debug=False)