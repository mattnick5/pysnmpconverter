import socket
from pysnmp.proto import rfc1902


def forward_trap(received_trap, forward_host, forward_port):
    forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    forward_socket.sendto(received_trap, (forward_host, forward_port))
    print "Forwarded " + str(forward_host) + ":" + str(forward_port)
        # print(f"Trap forwarded to {forward_host}:{forward_port}")


def receive_trap(listen_host, listen_port, forward_host1, forward_port1, forward_host2, forward_port2):
    print listen_host + ":" + str(listen_port)
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind((listen_host, listen_port))
    # print(f"Listening for traps on {listen_host}:{listen_port}")

    while True:
        received_trap, addr = listen_socket.recvfrom(4096)
        # print(f"Received trap from {addr[0]}:{addr[1]}")
        # Forward the received trap to another host
        forward_trap(received_trap, forward_host1, forward_port1)
        forward_trap(received_trap, forward_host2, forward_port2)


# Example usage
receive_trap('172.22.42.75', 163, '172.16.5.77', 162, '172.16.5.77', 162)
