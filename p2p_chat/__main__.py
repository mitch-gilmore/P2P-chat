import argparse
import socket

from p2p_chat.server import Server
from p2p_chat.client import Client

def run(command: str, **kwargs) -> None:

	match command:
		case 'server':
			server = Server(kwargs['port'])
			server.start()

		case 'client':
			Client(**kwargs)

		case _:
			raise ValueError(f"Invalid command: {command}")

def main():
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers(dest='command')

	server_parser = subparsers.add_parser('server')
	server_parser.add_argument('-p', '--port', type=int, help='The port of the server', default=1234)

	client_parser = subparsers.add_parser('client')
	client_parser.add_argument('username', type=str, help='The username of the client')
	client_parser.add_argument('client_port', type=int, help='The port of the client')
	client_parser.add_argument('-i', '--server_ip', type=str, help='The IP address of the server', default=socket.gethostname())
	client_parser.add_argument('-p', '--server_port', type=int, help='The port of the server', default=1234)

	run(**vars(parser.parse_args()))
