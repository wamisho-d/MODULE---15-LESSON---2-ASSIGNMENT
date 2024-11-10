from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Task 1: Initialize the HashMap to store messages by author
message_storage = {}

# Task 2: Function to handle storing messages in message_storage
def handle_message(author, message):
    if author not in message_storage:
        message_storage[author] = []  # Initialize list if author key doesn't exist
    message_storage[author].append(message)  # Append message to author's list

# Task 3: Event handler for 'message' event
@socketio.on('message')
def on_message(data):
    author = data.get("user")
    message = data.get("message")

    if not author or not message:
        return jsonify({"error": "Both 'user' and 'message' fields are required"}), 400

    # Store the message
    handle_message(author, message)
    
    # Emit the message to all connected clients
    emit('message', {'user': author, 'message': message}, broadcast=True)

# Task 5: Route to retrieve all messages by a specific user
@app.route('/get_all_messages/<user>', methods=['GET'])
def get_all_messages(user):
    messages = message_storage.get(user, [])
    return jsonify({"user": user, "messages": messages})

# Test endpoint for sending a test message (useful for testing in Postman)
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user = data.get('user')
    message = data.get('message')

    # Manually trigger the socketio message event
    socketio.emit('message', {'user': user, 'message': message})
    return jsonify({"status": "Message sent successfully"}), 200

if __name__ == '__main__':
    socketio.run(app)

# Testing in Postman

    # Send a POST request to /send_message with JSON:

{
   "user": "JohnDoe",
   "message": "Hello world!"
}

# To retrieve messages for a specific user, make a GET request to /get_all_messages/JohnDoe.
