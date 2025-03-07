from flask import Flask, request, jsonify

app = Flask(__name__)
data_store = {}  # Хранение данных по кодам

@app.route('/send', methods=['POST'])
def send_data():
    data = request.json
    code = data.get('code')
    content = data.get('data')
    if code and content:
        data_store[code] = content
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/receive', methods=['GET'])
def receive_data():
    code = request.args.get('code')
    if code in data_store:
        return jsonify(data_store[code]), 200
    return jsonify({"status": "error", "message": "Code not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)