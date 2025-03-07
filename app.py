from flask import Flask, request, jsonify
import json

app = Flask(__name__)
data_store = {}  # Хранение данных по кодам

@app.route('/send', methods=['POST'])
def send_data():
    try:
        data = request.json
        code = data.get('code')
        content = data.get('data')
        if code and content:
            print(f"Storing data for code {code}")  # Логирование
            data_store[code] = content  # Сохраняем данные как словарь
            return jsonify({"status": "success"}), 200
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    except Exception as e:
        print(f"Error in send_data: {e}")  # Логирование ошибок
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/receive', methods=['GET'])
def receive_data():
    try:
        code = request.args.get('code')
        print(f"Receiving data for code {code}")  # Логирование
        if code in data_store:
            data = data_store[code]
            return jsonify(data), 200
        return jsonify({"status": "error", "message": "Code not found"}), 404
    except Exception as e:
        print(f"Error in receive_data: {e}")  # Логирование ошибок
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
