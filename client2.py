import socket
import ast
import pegband_player2
import multiprocessing
import time

def receive_full_message(sock, buffer_size=4096):
    """Receive a complete message from the socket."""
    data = b''
    while True:
        chunk = sock.recv(buffer_size)
        if not chunk:
            break
        data += chunk
        # Check if we have a complete list by trying to parse it
        try:
            ast.literal_eval(data.decode())
            break  # Successfully parsed, we have the complete message
        except (SyntaxError, ValueError):
            # Not complete yet, continue receiving
            continue
    return data.decode()

# Connect to the server
server_ip = '0.0.0.0'
server_port = 4000
player = pegband_player2.PegbandPlayer2("Enter your name", 0, 0, [], 0, 0, 0)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
client_socket.send(str(player.name).encode())
global remaining_time
remaining_time = 120

# Receive board size and peg placement phase information
board_info = client_socket.recv(2048).decode().strip().split()

#Information for client
board_length = int(board_info[0])
board_width = int(board_info[1])
num_pegs = int(board_info[2])
num_rubberbands = int(board_info[3])
board = []

def run_with_timeout(func, player):

    def wrapper():
        #nonlocal remaining_time
        start_time = time.time()
        func()
        end_time = time.time()
        elapsed_time = end_time - start_time
        remaining_time -= elapsed_time

    p = multiprocessing.Process(target=wrapper)
    p.start()
    p.join(remaining_time)
    if p.is_alive():
        p.terminate()
        print(f"Time limit has been exceeded by {player.name}!")
        # Close the client socket
        client_socket.close()
    else:
        print(f"{player.name}, Remaining time: {remaining_time} seconds.")


#Information for players
player.board_length = int(board_info[0])
player.board_width = int(board_info[1])
player.num_pegs = int(board_info[2])
player.num_rubberbands = int(board_info[3])
player.player_color = int(board_info[4])

# Implement the peg placement phase (repeat for num_pegs rounds)
for round in range(num_pegs):
    # Receive the current board with peg positions
    board_str = receive_full_message(client_socket)
    board = ast.literal_eval(board_str)
    player.board = board
    # Choose a position to place a peg
    position = player.place_pegs()
    # Send the chosen peg position to the server
    client_socket.send(str(position).encode())

for round in range(num_rubberbands):
    # Receive the current board with peg and rubberband positions
    board_str = client_socket.recv(2048).decode()
    player.board = ast.literal_eval(board_str)
    start_time = time.time()
    rubberband_positions = player.place_rubberbands()
    end_time = time.time()
    client_socket.send(str(rubberband_positions).encode())

# Receive final game results
try:
    final_message = client_socket.recv(1024).decode()
    print(final_message)
except Exception as e:
    print(f"Error receiving final message: {e}")

# Close the client socket
client_socket.close()