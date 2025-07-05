import socket
from threading import Thread

# Server's IP Address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # Port we want to use
separator_token = "<SEP>" # Indicates seprator between client name and message

# Intialize list/set of all connected client's sockets
client_sockets = set()
# Create a TCP Socket
s = socket.socket()
# make the port as resusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    This function keeps listening for a message from 'cs' socket.
    Whenever a message is recieved, broadcast it to all other connected clients.
    """
    while True:
        try:
            # Keep listening for a message from 'cs' socket.
            msg = cs.recv(1024).decode()
        except Exception as e:
            # Client no longer connected
            # Remove it from the set
            print(f"[!] Error: (e)")
            client_sockets.remove(cs)
        else:
            # If we recieved a message, replace the <SEP>
            # Token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
        # Iterate over all connected sockets
        for client_socket in client_sockets:
            # And send the message
            client_socket.send(msg.encode())

while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages.
    t = Thread(target=listen_for_client, args=(client_socket,))
    # Make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # Start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()