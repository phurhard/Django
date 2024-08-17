from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PORT = os.getenv('PORT', 5000)

@app.route('/register', methods=["POST"])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if username and password:
            return jsonify({
                "username": username,
                "password": password
                })
    except Exception as e:
        return jsonify(error=str(e.args[0]))
            
@app.route('/')
def status():
    return jsonify(message="Up and working well")


if __name__ == "__main__":
    app.run(port=PORT)
