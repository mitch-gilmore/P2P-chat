import argparse
import socket

def main():
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	server_parser = subparsers.add_parser('server')
	server_parser.add_argument('-p', '--port', type=int, help='The port of the server', default=1234)

	client_parser = subparsers.add_parser('client')
	client_parser.add_argument('username', type=str, help='The username of the client')
	client_parser.add_argument('port', type=int, help='The port of the client')
	client_parser.add_argument('-i', '--server_ip', type=str, help='The IP address of the server', default=socket.gethostname())
	client_parser.add_argument('-p', '--server_port', type=int, help='The port of the server', default=1234)

	args = parser.parse_args()