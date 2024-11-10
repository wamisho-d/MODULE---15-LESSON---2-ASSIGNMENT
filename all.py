# Task 1: Refactor the messages list to use a Hashmap called message_storage where the key is the author and the value is a list of messages.
# Define a Hashmap (Dictionary in Python): Initialize an empty dictionary to store messages with the author as the key and a list of messages as the value.

message_storage = {}

# Task 2: Modify the handle_message function to store messages in the message_storage Hashmap. 
# Modify Function to Store Messages: Update the handle_message function to add messages to the message_storage.

def handle_message(data):
    user = data['user']
    message = data['message']
    
    if user in message_storage:
        message_storage[user].append(message)
    else:
        message_storage[user] = [message]
    
# Task 3: Update the socketio.on('message') event handler to retrieve messages from the message_storage HashMap.
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('message')
def on_message(data):
    user = data.get('user')
    message = data.get('message')
    
    # Store the message
    handle_message(data)
    
    # Send acknowledgment back
    emit('response', {'status': 'message received'})