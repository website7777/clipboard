from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)
data_store = {}  # Хранение данных по кодам
message_status = {}  # Статус сообщений (получено или нет)

@app.route('/send', methods=['POST'])
def send_data():
    try:
        data = request.json
        code = data.get('code')
        content = data.get('data')
        message_id = f"{code}_{int(time.time() * 1000)}"  # Уникальный ID сообщения
        
        if code and content:
            print(f"Storing data for code {code}")  # Логирование
            data_store[code] = content  # Сохраняем данные как словарь
            message_status[code] = {'delivered': False, 'message_id': message_id}
            return jsonify({"status": "success", "message_id": message_id}), 200
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    except Exception as e:
        print(f"Error in send_data: {e}")  # Логирование ошибок
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/receive', methods=['GET'])
def receive_data():
    try:
        code = request.args.get('code')
        print(f"Receiving data for code {code}")  # Логирование
        
        if code in data_store and code in message_status:
            if not message_status[code]['delivered']:
                data = data_store[code]
                message_status[code]['delivered'] = True
                return jsonify(data), 200
            else:
                # Сообщение уже было доставлено
                return jsonify({"status": "no_new_messages"}), 204
        return jsonify({"status": "error", "message": "Code not found"}), 404
    except Exception as e:
        print(f"Error in receive_data: {e}")  # Логирование ошибок
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/ack', methods=['POST'])
def acknowledge_message():
    try:
        data = request.json
        code = data.get('code')
        message_id = data.get('message_id')
        
        if code in message_status and message_status[code]['message_id'] == message_id:
            message_status[code]['delivered'] = True
            return jsonify({"status": "success"}), 200
        return jsonify({"status": "error", "message": "Invalid message ID"}), 400
    except Exception as e:
        print(f"Error in acknowledge_message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
